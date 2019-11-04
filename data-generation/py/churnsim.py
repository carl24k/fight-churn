
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
import random
from postgres import Postgres
from math import ceil
import os
import tempfile

from customer import Customer
from behavior import GaussianBehaviorModel
from utility import UtilityModel


class ChurnSimulation:

    def __init__(self, model, start, end, init_customers, growth, churn, mrr,seed):
        '''
        Creates the behavior/utility model objects, sets internal variables to prepare for simulation, and creates
        the database connection

        :param model: name of the behavior/utility model parameters
        :param start: start date for simulation
        :param end: end date for simulation
        :param init_customers: how many customers to create at start date
        :param growth: monthly customer growth rate
        :param churn: monthly customer churn rate
        :param mrr: customer MRR
        '''

        self.model_name=model
        self.start_date = start
        self.end_date = end
        self.init_customers=init_customers
        self.monthly_growth_rate = growth
        self.monthly_churn_rate = churn
        self.mrr=mrr

        self.behave_mod=GaussianBehaviorModel(self.model_name,seed)
        self.util_mod=UtilityModel(self.model_name,self.monthly_churn_rate,self.behave_mod)

        self.subscription_count = 0
        self.tmp_sub_file_name='%s/%s_tmp_sub.csv' % ( tempfile.gettempdir(),self.model_name)
        self.tmp_event_file_name='%s/%s_tmp_event.csv' % ( tempfile.gettempdir(), self.model_name)

        self.db = Postgres("postgres://%s:%s@localhost/%s" % (
        os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))

    def remove_tmp_files(self):
        '''
        Remove temp files when the simulation is over
        :return:
        '''
        os.remove(self.tmp_event_file_name)
        os.remove(self.tmp_sub_file_name)

    def simulate_customer(self, start_of_month):
        '''
        Simulate one customer collecting its events and subscriptions.

        This function has the core interaction between the simulation objects.  Customer is created from the behavior
        model, and picking a random start date within the month.  Then the customer objects simulates the events for
        the month, and the utility model determines if there is a churn based on the simulated event counts.

        :param start_of_month:
        :return: the new customer object it contains the events and subscriptions
        '''
        new_customer=self.behave_mod.generate_customer()

        # Pick a random start date for the subscription within the month
        end_range = start_of_month + relativedelta(months=+1)
        this_month=start_of_month + timedelta(days=random.randrange((end_range-start_of_month).days))

        churned = False
        while not churned:
            next_month=this_month+relativedelta(months=1)
            new_customer.subscriptions.append( (this_month,next_month) )
            month_count = new_customer.generate_events(this_month,next_month)
            churned=self.util_mod.simulate_churn(month_count) or next_month > self.end_date
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

        for i in range(n_to_create):
            customer = self.simulate_customer(month_date)
            self.copy_customer_to_database(customer)
            print('Simulated customer %d: %d subscription, %d events' %
                  (i, len(customer.subscriptions), len(customer.events)))


    def copy_customer_to_database(self,customer):
        '''
        Copy one customers data to the database, by first writing it to temp files and then using the sql COPY command
        :param customer: a Customer object that has already had its simulation run
        :return:
        '''
        with open(self.tmp_sub_file_name, 'w') as tmp_file:
            for s in customer.subscriptions:
                tmp_file.write("%d,%d,'%s','%s','%s',%f,\\null,\\null,1\n" % \
                               (self.subscription_count, customer.id, self.model_name, s[0], s[1], self.mrr))
                self.subscription_count += 1
        with open(self.tmp_event_file_name, 'w') as tmp_file:
            for e in customer.events:
                tmp_file.write("%d,'%s',%d\n" % (customer.id, e[0], e[1]))
        sql = "COPY %s.subscription FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (
        self.model_name, self.tmp_sub_file_name)
        self.db.run(sql)
        sql = "COPY %s.event FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (
        self.model_name, self.tmp_event_file_name)
        self.db.run(sql)

    def truncate_old_sim(self):
        '''
        Removes an old simulation from the database, if it already exists for this model
        :return: True if is safe to proceed (no data or data removed); False means old data not removed
        '''
        oldEvent= self.db.one('select count(*) from %s.event' % self.model_name)
        oldSubs= self.db.one('select count(*) from %s.subscription' % self.model_name)
        if oldEvent > 0 or oldSubs>0:
            print('TRUNCATING *Events & Subscriptions* in schema -> %s <-  ...' % self.model_name)
            if input("are you sure? (enter %s to proceed) " % self.model_name) == self.model_name:
                if oldEvent > 0:
                    self.db.run('truncate table %s.event' % self.model_name)
                if oldSubs > 0:
                    self.db.run('truncate table %s.subscription' % self.model_name)
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
        self.behave_mod.insert_event_types(self.model_name,self.db)

        # Initial customer count
        print('\nCreating %d initial customers for %s start date' % (self.init_customers,self.start_date))
        self.create_customers_for_month(self.start_date,self.init_customers)
        print('Created %d initial customers with %d subscriptions for start date %s' % (self.init_customers,self.subscription_count,str(self.start_date)))

        # Advance to additional months
        next_month=self.start_date+relativedelta(months=+1)
        n_to_add = int(ceil( self.init_customers* self.monthly_growth_rate))  # number of new customers in first month
        while next_month < self.end_date:
            print('\nCreating %d new customers for month %s:' % (n_to_add,next_month))
            self.create_customers_for_month(next_month,n_to_add)
            print('Created %d new customers for month %s, now %d subscriptions\n' % (n_to_add,str(next_month),self.subscription_count))
            next_month=next_month+relativedelta(months=+1)
            n_to_add = int(ceil( n_to_add * (1.0+self.monthly_growth_rate))) # increase the new customers by growth

        self.remove_tmp_files()

if __name__ == "__main__":

    model_name = 'soc_net_sim_1'
    start = date(2020, 1, 1)
    end = date(2020, 6, 1)
    init = 10000
    growth_rate = 0.15
    churn_rate = 0.10
    mrr = 9.99
    random_seed = None
    if random_seed is not None:
        random.seed(random_seed) # for random


    churn_sim = ChurnSimulation(model_name, start, end, init,growth_rate,churn_rate, mrr,random_seed)
    churn_sim.run_simulation()

