import math
from collections import deque
from datetime import date, timedelta, datetime
from dateutil import parser
from dateutil.relativedelta import *
import random
from postgres import Postgres
from math import ceil
from shutil import copyfile

import argparse
from filelock import FileLock
import os

from joblib import Parallel, delayed
import json
import glob
import pandas as pd
import numpy as np
import psycopg2 as post
import tempfile

from fightchurn.datagen.behavior import FatTailledBehaviorModel
from fightchurn.datagen.churndb import drop_schema, setup_churn_db
from fightchurn.datagen.utility import UtilityModel
from fightchurn.datagen.customer import  Customer

class ChurnSimulation:

    def __init__(self, args):
        '''
        Creates the behavior/utility model objects, sets internal variables to prepare for simulation, and creates
        the database connection

        :param model: name of the behavior/utility model parameters
        :param start: start date for simulation
        :param end: end date for simulation
        :param init_customers: how many customers to create at start date
        '''
        self.args = args
        self.model_name=args.model
        self.start_date = parser.parse(args.start_date).date()
        self.end_date = parser.parse(args.end_date).date()
        self.init_customers=args.init_customers
        self.monthly_growth_rate = args.growth_rate
        self.devmode= args.dev
        self.n_parallel = args.n_parallel
        self.utility_dist = []
        print(f'Simulating with {self.n_parallel} parallel processes...')
        self.util_mod=UtilityModel(self.model_name,contrib_scale=self.args.util_contrib_scale)
        local_dir = f'{os.path.abspath(os.path.dirname(__file__))}/conf/'

        self.min_age = args.min_age
        self.max_age = args.max_age
        self.age_satisfaction_scale = args.age_satisfy
        # self.age_range = self.max_age-self.min_age
        # self.avg_age = (self.max_age+self.min_age)/20

        self.behavior_models = {}
        self.model_list = []
        pop_file = os.path.join(local_dir, f"{self.model_name}_population.csv")
        self.population_percents = pd.read_csv(pop_file, index_col=0)

        for version in self.population_percents.index.values:
            behave_mod=FatTailledBehaviorModel(self.model_name, exp_base=self.args.behave_exp_base,
                                               random_seed= args.random_seed, version= version)
            self.behavior_models[behave_mod.version]=behave_mod
            self.model_list.append(behave_mod)

        local_dir = f'{os.path.abspath(os.path.dirname(__file__))}/conf/'

        plans_path = local_dir +self.model_name + '_plans.csv'
        self.plans = pd.read_csv(plans_path,index_col=0)
        self.plans = self.plans.sort_values('mrr',ascending=True) # Make sure its sorted by increasing MRR
        add_on_file = local_dir +self.model_name + '_addons.csv'
        if os.path.exists(add_on_file):
            self.add_ons = pd.read_csv(add_on_file)
        else:
            self.add_ons = pd.DataFrame()
        self.util_mod.setExpectations(self.behavior_models,self.population_percents)
        self.population_picker = np.cumsum(self.population_percents)

        self.country_lookup = pd.read_csv(local_dir +self.model_name + '_country.csv')

        self.tmp_sub_file_name = os.path.join(tempfile.gettempdir(),f'{self.model_name}_tmp_sub.csv')
        self.tmp_event_file_name=os.path.join(tempfile.gettempdir(),f'{self.model_name}_tmp_event.csv')

        self.save_path = os.path.join(os.getenv('CHURN_OUT_DIR') , self.model_name )
        os.makedirs(self.save_path, exist_ok=True)
        copy_path = os.path.join(self.save_path,  f'{self.model_name}_plans.csv')
        copyfile(plans_path, copy_path)
        copy_path = os.path.join(self.save_path,  f'{self.model_name}_addons.csv')
        copyfile(add_on_file, copy_path)
        arg_path = os.path.join(self.save_path, f'{self.model_name}_args.json')
        with open(arg_path, 'w') as f:
            json.dump(args.__dict__, f, indent=2)


    def con_string(self):
        return f"postgresql://{os.environ.get('CHURN_DB_HOST','localhost')}/{os.environ['CHURN_DB']}?user={os.environ['CHURN_DB_USER']}&password={os.environ['CHURN_DB_PASS']}"


    def sim_rate_debug_query(self):

        file_root = os.path.abspath(os.path.dirname(__file__))
        with open(f'{file_root}/schema/churn_by_plan.sql', 'r') as sqlfile:
            sql = sqlfile.read().replace('\n', ' ')
        sql = sql.replace('%schema',self.model_name)
        with FileLock(Customer.ID_LOCK_FILE):
            db = Postgres(self.con_string())
            res = pd.DataFrame(db.all(sql))
            print(res)


    def remove_tmp_files(self):
        '''
        Remove temp files. Runs at the start in case a previous run failed, and at the end.
        :return:
        '''
        try:
            os.remove(Customer.ID_LOCK_FILE)
        except OSError:
            pass
        try:
            os.remove(Customer.ID_FILE)
        except OSError:
            pass

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
        new_customer=customer_model.generate_customer(start_of_month,args=args)

        customer_country = np.random.choice(self.country_lookup['country'],p=self.country_lookup['pcnt'])
        new_customer.country = customer_country

        plans_to_use = self.plans
        available_periods = None
        if 'bill_period' in self.plans.columns.values:
            available_periods = sorted(self.plans['bill_period'].unique())
            # For the first month in a simulation, only allow 1 month bill periods
            #  - otherwise there are artificial cycles of lots of people re-newing on the 3,6,12 months
            if start_of_month==self.start_date:
                min_period=self.plans['bill_period'].min()
                plans_to_use =  self.plans[self.plans['bill_period']==min_period]

        new_customer.pick_initial_plan(plans_to_use, self.add_ons, available_periods)

        # Pick a random start date for the subscription within the month
        end_range = start_of_month + relativedelta(months=+1)
        customer_start = start_of_month + timedelta(days=random.randrange((end_range-start_of_month).days))
        next_renewal = customer_start + relativedelta(months=new_customer.bill_period)

        def add_customer_subscriptions(this_month, next_renewal):
            plan_units, plan_quantity = self.get_unit_quantity(new_customer.plan)
            new_customer.subscriptions.append( (new_customer.plan, this_month,
                                                next_renewal,
                                                new_customer.base_mrr, plan_quantity, plan_units, new_customer.bill_period, new_customer.discount ))
            for add_on in new_customer.add_ons.iterrows():
                add_units, add_quantity = self.get_unit_quantity(add_on[1]['plan'])
                new_customer.subscriptions.append( (add_on[1]['plan'],this_month,next_renewal, add_on[1]['mrr'],
                                                    add_quantity,add_units, new_customer.bill_period, new_customer.discount) )

        add_customer_subscriptions(customer_start, next_renewal)

        churned = False
        churn_intent_count = 0
        num_bill_periods = 1
        num_months = 0
        num_months_this_bill_period = 0
        while not churned:
            this_month = customer_start if num_months == 0 else next_month
            num_months += 1
            num_months_this_bill_period += 1
            next_month=customer_start+relativedelta(months=num_months)
            month_event_count = new_customer.generate_events(this_month,next_month)
            _ = self.util_mod.utility_function(month_event_count,new_customer)
            churn_intent = False
            if args.acausal_churn > 0:
                if random.uniform(0,1) < args.acausal_churn:
                    churn_intent = True
            if not churn_intent:
                churn_intent =self.util_mod.simulate_churn(month_event_count,new_customer)
            if churn_intent:
                churn_intent_count += 1
            # exit if the simulation is over
            if next_month > self.end_date:
                break
            # check for churn, upgrade/downgrade on renewal date, make new subscriptions if not churned
            elif next_month >= next_renewal:
                # churn at the end of the term if they wanted to churn just once (every month for monthly)
                if churn_intent > 0:
                    churned = True
                if not churned:
                    churn_intent_count = 0
                    num_months_this_bill_period = 0
                    bill_period_change = self.util_mod.simulate_upgrade_downgrade(month_event_count,new_customer,self.plans,self.add_ons)
                    if bill_period_change:
                        customer_start = next_month
                        num_months=0
                        num_bill_periods=1
                    else:
                        num_bill_periods += 1
                    next_renewal = customer_start + relativedelta(months=new_customer.bill_period * num_bill_periods)
                    add_customer_subscriptions(next_month,next_renewal)
            elif (churn_intent_count > 1 and 2 <= new_customer.bill_period <= 6) or \
                (churn_intent_count > 2 and 6 < new_customer.bill_period):
                # churn mid term on 2 churns for quarterly/bi-annual, 3 churns for annual
                churned=True
                old_last = new_customer.subscriptions[-1]
                new_last = (old_last[0],old_last[1],next_month,old_last[3],old_last[4],old_last[5], old_last[6], old_last[7])
                new_customer.subscriptions[-1]= new_last

        return new_customer

    def get_unit_quantity(self,plan):
        if plan in self.plans.index.values:
            if self.plans.shape[1]>2:
                limit_col = self.plans.columns.values[2]
                return  limit_col,  self.plans.loc[plan,limit_col]

        if plan in self.add_ons['plan'].values:
            if self.add_ons.shape[1]>3:
                add_on = self.add_ons[self.add_ons['plan']==plan]
                for limit_col in self.add_ons.columns.values[3:]:
                    if add_on[limit_col].values[0]>0:
                        return limit_col, add_on[limit_col].values[0]

        return None, None

    def create_customers_for_month(self,month_date,n_to_create):
        '''
        Creates all the customers for one month, by calling simulate_customer and copy_customer_to_database in a loop.
        :param month_date: the month start date
        :param n_to_create: number of customers to create within that month
        :return:
        '''

        def create_one_customer():
            customer = self.simulate_customer(month_date)
            self.copy_customer_to_database(customer)
            if self.devmode and customer.id> 0 and (customer.id % round(self.init_customers / 10)) == 0:
                self.sim_rate_debug_query()
            res = np.append(customer.utility_contribs, customer.current_utility)
            return res

        contribs = Parallel(n_jobs=self.n_parallel)(delayed(create_one_customer)() for i in range(n_to_create))

        if self.devmode:
            self.utility_dist.extend(contribs)
            util_names = list(self.util_mod.behave_names)
            util_names.extend(['mrr','utility'])
            utility_obs = pd.DataFrame(self.utility_dist, columns=util_names)
            utility_obs.to_csv( os.path.join(self.save_path,f'utility_contribs_{datetime.strftime(month_date,"%Y%m%d")}.csv'))
            utility_desc=pd.DataFrame(utility_obs.describe())
            utility_desc.to_csv( os.path.join(self.save_path,f'utility_contribs_{datetime.strftime(month_date,"%Y%m%d")}_summary.csv'))

    def copy_customer_to_database(self,customer):
        '''
        Copy one customers data to the database, by first writing it to temp files and then using the sql COPY command
        :param customer: a Customer object that has already had its simulation run
        :return:
        '''
        sub_file_name = self.tmp_sub_file_name.replace('.csv', f'{customer.id}.csv')
        event_file_name = self.tmp_event_file_name.replace('.csv', f'{customer.id}.csv')
        db = Postgres(self.con_string())

        with open(sub_file_name, 'w') as tmp_file:
            for s in customer.subscriptions:
                # plan name, start, end, mrr, quantity, units, billing period, discount
                tmp_file.write(f'{customer.id},{s[0]},{s[1]},{s[2]},{s[3]},'
                               f'{s[4] if s[4] is not None else "NULL"},{s[5] if s[5] is not None else "NULL"},'
                               f'{s[6]},{s[7]}\n')
        with open(event_file_name, 'w') as tmp_file:
            for e in customer.events:
                tmp_file.write(f'{customer.id},{e[0]},{e[1]},{e[2]},{e[3] if e[3] is not None else "NULL"}\n') # event time, event type id, user id, value

        sql = "INSERT INTO {}.account VALUES({},'{}','{}',{})".format(self.model_name, customer.id, customer.channel,
                                                                customer.date_of_birth.isoformat(),
                                                                'NULL' if customer.country == 'None' else "'{}'".format(
                                                                    customer.country))

        db.run(sql)

        con = post.connect( database= os.environ['CHURN_DB'],
                                 user= os.environ['CHURN_DB_USER'],
                                 password=os.environ['CHURN_DB_PASS'],
                                 host=os.environ.get('CHURN_DB_HOST','localhost'))
        cur = con.cursor()

        sql = "COPY %s.subscription FROM STDIN USING DELIMITERS ',' WITH NULL AS 'NULL'" % (self.model_name)
        with open(sub_file_name, 'r') as f:
            cur.copy_expert(sql, f)
        con.commit()

        sql = "COPY %s.event FROM STDIN USING DELIMITERS ',' WITH NULL AS 'NULL'" % (self.model_name)
        with open(event_file_name, 'r') as f:
            cur.copy_expert(sql, f)
        con.commit()
        con.close()

        os.remove(event_file_name)
        os.remove(sub_file_name)


    def truncate_old_sim(self):
        '''
        Removes an old simulation from the database, if it already exists for this model
        :return: True if is safe to proceed (no data or data removed); False means old data not removed
        '''
        db= Postgres(self.con_string())

        exists = db.one(f"SELECT exists(select schema_name FROM information_schema.schemata WHERE schema_name = '{self.model_name}')")
        if exists:
            print('TRUNCATING *Events/Metrics & Subscriptions/Observations* in schema -> %s <-  ...' % self.model_name)
            if input("are you sure? (enter %s to proceed) " % self.model_name) == self.model_name:
                drop_schema(self.model_name)
                setup_churn_db(self.model_name)
                return True
            else:
                return False
        else:
            setup_churn_db(self.model_name)
            return True


    def run_simulation(self, force=False):
        '''
        Simulation main function. First it prepares the database by truncating any old events and subscriptions, and
        inserting the event types into the database.  Next it creeates the initial customers by calling
        create_customers_for_month, and then it advances month by month adding new customers (also using
        create_customers_for_month.)  The number of new customers for each month is determined from the growth rate.
        Note that churn is not handled at this level, but is modeled at the customer level.
        :return:
        '''

        # database setup
        if not force and not self.truncate_old_sim():
            return
        self.remove_tmp_files()

        # Any model can insert the event types
        db = Postgres(self.con_string())
        self.behavior_models[next(iter(self.behavior_models))].insert_event_types(self.model_name,db)

        # Initial customer count
        print('\nCreating %d initial customers for month of %s' % (self.init_customers,self.start_date))
        self.create_customers_for_month(self.start_date,self.init_customers)
        print('Created %d initial customers for start date %s' % (self.init_customers,str(self.start_date)))

        # Advance to additional months
        next_month=self.start_date+relativedelta(months=+1)
        n_to_add = int(ceil( self.init_customers* self.monthly_growth_rate))  # number of new customers in first month
        while next_month < self.end_date:
            print('\nCreating %d new customers for month of %s:' % (n_to_add,next_month))
            self.create_customers_for_month(next_month,n_to_add)
            print('Created %d new customers for month %s\n' % (n_to_add,str(next_month)))
            next_month=next_month+relativedelta(months=+1)
            n_to_add = int(ceil( n_to_add * (1.0+self.monthly_growth_rate))) # increase the new customers by growth

        self.remove_tmp_files()
        self.sim_rate_debug_query()

def run_churn_simulation(args):
    if args.random_seed is not None:
        random.seed(args.random_seed) # for random
    churn_sim = ChurnSimulation(args)
    churn_sim.run_simulation(force=args.force)

def churn_args(parse_command_line=True):
    parser = argparse.ArgumentParser()
    # Default arguments
    parser.add_argument("--random_seed", type=int, help="Seed for random")
    parser.add_argument("--model", type=str, help="The name of the schema", default='socialnet7')
    parser.add_argument("--start_date", type=str, help="The name of the schema", default='2020-01-01')
    parser.add_argument("--end_date", type=str, help="The name of the schema", default='2020-06-01')

    parser.add_argument("--force", type=bool, help="Flag to force over-write old data", default=False)
    parser.add_argument("--dev", action="store_true", default=False,help="Dev mode: Extra debug info/options")
    parser.add_argument("--n_parallel", type=int, help="Number of parallel cpus for simulation", default=1)

    parser.add_argument("--init_customers", type=int, help="Starting customers", default=10000)
    parser.add_argument("--growth_rate", type=float, help="New customer growth rate", default=0.1)
    parser.add_argument("--acausal_churn", type=float, help="Churn rate for no reason", default=0.0)

    parser.add_argument("--satisfy_scale", type=float, help="Random satisfaction scaling factor", default=1.5)
    parser.add_argument("--satisfy_base", type=float, help="Random satisfaction scaling base", default=2.0)

    parser.add_argument("--min_age", type=int, help="Minimum customer age", default=12)
    parser.add_argument("--max_age", type=int, help="Maximum customer age", default=82)
    parser.add_argument("--age_satisfy", type=float, help="Age satisfaction scacling coefficient", default=0.5)


    parser.add_argument("--min_discount", type=float, help="Minimum discount", default=0.05)
    parser.add_argument("--max_discount", type=float, help="Maximum discount", default=0.5)
    parser.add_argument("--discount_prob", type=float, help="Discount Probability", default=0.5)

    parser.add_argument("--weekday_scale", type=float, help="Action rate scaling for weekedays", default=0.8)
    parser.add_argument("--weekend_scale", type=float, help="Action rate scaling for weekends", default=1.2)

    parser.add_argument("--behave_exp_base", type=float, help="Base of exponent used in behavior model", default=1.6)
    parser.add_argument("--util_contrib_scale", type=float, help="Scaling factor for utility contributions", default=2.0)


    if parse_command_line:
        # actually parse command line
        the_args, _ = parser.parse_known_args()
    else:
        # Just return defaults
        the_args = parser.parse_args([])

    return the_args

if __name__ == "__main__":

    args = churn_args()
    run_churn_simulation(args)
