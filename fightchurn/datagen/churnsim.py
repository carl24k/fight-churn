
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
import random
from postgres import Postgres
from math import ceil
import os
import glob
import sys
import tempfile
import pandas as pd
import numpy as np
import psycopg2 as post

from fightchurn.datagen.behavior import FatTailledBehaviorModel
from fightchurn.datagen.utility import UtilityModel


class ChurnSimulation:

    def __init__(self, model, start, end, init_customers,seed):
        '''
        Creates the behavior/utility model objects, sets internal variables to prepare for simulation, and creates
        the database connection

        :param model: name of the behavior/utility model parameters
        :param start: start date for simulation
        :param end: end date for simulation
        :param init_customers: how many customers to create at start date
        '''

        self.model_name=model
        self.start_date = start
        self.end_date = end
        self.init_customers=init_customers
        self.monthly_growth_rate = 0.1

        self.util_mod=UtilityModel(self.model_name)
        local_dir = f'{os.path.abspath(os.path.dirname(__file__))}/conf/'
        behavior_versions = glob.glob(local_dir+self.model_name+'_*.csv')
        self.behavior_models = {}
        self.model_list = []
        for b in behavior_versions:
            version = b[(b.find(self.model_name) + len(self.model_name)+1):-4]
            if version in ('utility','population','country'):
                continue
            behave_mod=FatTailledBehaviorModel(self.model_name,seed,version)
            self.behavior_models[behave_mod.version]=behave_mod
            self.model_list.append(behave_mod)

        local_dir = f'{os.path.abspath(os.path.dirname(__file__))}/conf/'
        if len(self.behavior_models)>1:
            self.population_percents = pd.read_csv(local_dir +self.model_name + '_population.csv',index_col=0)
        self.util_mod.setChurnScale(self.behavior_models,self.population_percents)
        self.population_picker = np.cumsum(self.population_percents)

        self.country_lookup = pd.read_csv(local_dir +self.model_name + '_country.csv')

        self.subscription_count = 0
        self.tmp_sub_file_name = os.path.join(tempfile.gettempdir(),'{}_tmp_sub.csv'.format(self.model_name))
        self.tmp_event_file_name=os.path.join(tempfile.gettempdir(),'{}_tmp_event.csv'.format(self.model_name))

        self.db = Postgres("postgres://%s:%s@localhost/%s" % (
        os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))

        self.con = post.connect( database= os.environ['CHURN_DB'],
                                 user= os.environ['CHURN_DB_USER'],
                                 password=os.environ['CHURN_DB_PASS'])

    def remove_tmp_files(self):
        '''
        Remove temp files when the simulation is over
        :return:
        '''
        os.remove(self.tmp_event_file_name)
        os.remove(self.tmp_sub_file_name)

    def pick_customer_model(self):
        choice = random.uniform(0,1)
        for m in range(0,self.population_picker.shape[0]):
            if choice <= self.population_picker['percent'][m]:
                version_name=self.population_picker.index.values[m]
                return self.behavior_models[version_name]


    def simulate_customer(self, start_of_month):
        '''
        Simulate one customer collecting its events and subscriptions.

        This function has the core interaction between the simulation objects.  Customer is created from the behavior
        model, and picking a random start date within the month.  Then the customer objects simulates the events for
        the month, and the utility model determines if there is a churn based on the simulated event counts.

        :param start_of_month:
        :return: the new customer object it contains the events and subscriptions
        '''
        # customer_model = self.pick_customer_model()
        customer_model = np.random.choice(self.model_list,p=self.population_percents['pcnt'])
        new_customer=customer_model.generate_customer(start_of_month)

        customer_country = np.random.choice(self.country_lookup['country'],p=self.country_lookup['pcnt'])
        new_customer.country = customer_country

        # Pick a random start date for the subscription within the month
        end_range = start_of_month + relativedelta(months=+1)
        this_month=start_of_month + timedelta(days=random.randrange((end_range-start_of_month).days))

        churned = False
        while not churned:
            next_month=this_month+relativedelta(months=1)
            new_customer.subscriptions.append( (this_month,next_month) )
            month_count = new_customer.generate_events(this_month,next_month)
            churned=self.util_mod.simulate_churn(month_count,new_customer) or next_month > self.end_date
            if not churned:
                this_month = next_month
        return new_customer


    def create_customers_for_month(self,month_date,n_to_create):
        '''
        Creates all the customers for one month, by calling simulate_customer and copy_customer_to_database in a loop.
        :param month_date: the month start date
        :param n_to_create: number of customers to create within that month
        :return:
        '''

        total_subscriptions=0
        total_events=0
        for i in range(n_to_create):
            customer = self.simulate_customer(month_date)
            self.copy_customer_to_database(customer)
            total_subscriptions+=len(customer.subscriptions)
            total_events+=len(customer.events)
            if i % 100==0:
                print('Simulated customer {}/{}: {:,} subscriptions & {:,} events'.format(i,n_to_create, total_subscriptions, total_events))


    def copy_customer_to_database(self,customer):
        '''
        Copy one customers data to the database, by first writing it to temp files and then using the sql COPY command
        :param customer: a Customer object that has already had its simulation run
        :return:
        '''
        with open(self.tmp_sub_file_name, 'w') as tmp_file:
            for s in customer.subscriptions:
                tmp_file.write("%d,%d,'%s','%s','%s',%f,\\null,\\null,1\n" % \
                               (self.subscription_count, customer.id, self.model_name, s[0], s[1], 9.99)) # mrr is 9.99
                self.subscription_count += 1
        with open(self.tmp_event_file_name, 'w') as tmp_file:
            for e in customer.events:
                tmp_file.write("%d,'%s',%d\n" % (customer.id, e[0], e[1]))

        sql =         "INSERT INTO {}.account VALUES({},'{}','{}',{})".format(self.model_name, customer.id, customer.channel,
                                                                customer.date_of_birth.isoformat(),
                                                                'NULL' if customer.country == 'None' else "'{}'".format(
                                                                    customer.country))
        self.db.run(sql)

        cur = self.con.cursor()

        sql = "COPY %s.subscription FROM STDIN USING DELIMITERS ',' WITH NULL AS '\\null'" % (self.model_name)
        with open(self.tmp_sub_file_name, 'r') as f:
            cur.copy_expert(sql, f)
        self.con.commit()

        sql = "COPY %s.event FROM STDIN USING DELIMITERS ',' WITH NULL AS '\\null'" % (self.model_name)
        with open(self.tmp_event_file_name, 'r') as f:
            cur.copy_expert(sql, f)
        self.con.commit()


    def truncate_old_sim(self):
        '''
        Removes an old simulation from the database, if it already exists for this model
        :return: True if is safe to proceed (no data or data removed); False means old data not removed
        '''
        oldEvent= self.db.one('select count(*) from %s.event' % self.model_name)
        oldSubs= self.db.one('select count(*) from %s.subscription' % self.model_name)
        oldAccount = self.db.one('select count(*) from %s.account' % self.model_name)
        if oldEvent > 0 or oldSubs>0 or oldAccount>0:
            print('TRUNCATING *Events/Metrics & Subscriptions/Observations* in schema -> %s <-  ...' % self.model_name)
            if input("are you sure? (enter %s to proceed) " % self.model_name) == self.model_name:
                if oldEvent > 0:
                    self.db.run('truncate table %s.event' % self.model_name)
                    self.db.run('truncate table %s.metric' % self.model_name)
                if oldAccount > 0:
                    self.db.run('truncate table %s.account' % self.model_name)
                if oldSubs > 0:
                    self.db.run('truncate table %s.subscription' % self.model_name)
                    self.db.run('truncate table %s.active_period' % self.model_name)
                    self.db.run('truncate table %s.observation' % self.model_name)
                return True
            else:
                return False
        else:
            return True

    def run_simulation(self):
        '''
        Simulation main function. First it prepares the database by truncating any old events and subscriptions, and
        inserting the event types into the database.  Next it creeates the initial customers by calling
        create_customers_for_month, and then it advances month by month adding new customers (also using
        create_customers_for_month.)  The number of new customers for each month is determined from the growth rate.
        Note that churn is not handled at this level, but is modeled at the customer level.
        :return:
        '''

        # database setup
        if not self.truncate_old_sim():
            return
        # Any model can insert the event types
        self.behavior_models[next(iter(self.behavior_models))].insert_event_types(self.model_name,self.db)

        # Initial customer count
        print('\nCreating %d initial customers for month of %s' % (self.init_customers,self.start_date))
        self.create_customers_for_month(self.start_date,self.init_customers)
        print('Created %d initial customers with %d subscriptions for start date %s' % (self.init_customers,self.subscription_count,str(self.start_date)))

        # Advance to additional months
        next_month=self.start_date+relativedelta(months=+1)
        n_to_add = int(ceil( self.init_customers* self.monthly_growth_rate))  # number of new customers in first month
        while next_month < self.end_date:
            print('\nCreating %d new customers for month of %s:' % (n_to_add,next_month))
            self.create_customers_for_month(next_month,n_to_add)
            print('Created %d new customers for month %s, now %d subscriptions\n' % (n_to_add,str(next_month),self.subscription_count))
            next_month=next_month+relativedelta(months=+1)
            n_to_add = int(ceil( n_to_add * (1.0+self.monthly_growth_rate))) # increase the new customers by growth

        self.remove_tmp_files()

def run_churn_simulation(model_name, start_date, end_date, init_customers, random_seed=None):
    if random_seed is not None:
        random.seed(random_seed) # for random
    churn_sim = ChurnSimulation(model_name, start_date, end_date, init_customers,random_seed)
    churn_sim.run_simulation()

if __name__ == "__main__":

    model_name = 'socialnet7'
    if len(sys.argv) >= 2:
        model_name = sys.argv[1]

    start_date = date(2020, 1, 1)
    end_date = date(2020, 6, 1)
    init_customers = 10000


    run_churn_simulation(model_name, start_date, end_date, init_customers)
