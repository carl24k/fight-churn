
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
from random import randrange
from postgres import Postgres
from math import ceil
import os

from customer import Customer
from behavior import GaussianBehaviorModel
from utility import UtilityModel

##########################################################################
# CONSTANTS

class ChurnSimulation:

    def __init__(self):

        self.model_name='test2'
        self.tmp_sub_file_name='/tmp/%s_tmp_sub.csv' % self.model_name
        self.tmp_event_file_name='/tmp/%s_tmp_event.csv' % self.model_name
        self.start_date = date(2019,1,1)
        self.end_date = date(2019,6,1)
        self.init_customers=500
        self.monthly_growth_rate = 0.05
        self.monthly_churn_rate = 0.04
        self.mrr=9.99
        self.behave_mod=GaussianBehaviorModel(self.model_name)
        self.util_mod=UtilityModel(self.model_name,self.monthly_churn_rate,self.behave_mod)
        self.subscription_count = 0


    def simulate_customer(self, start_of_month):
        events = []
        subscriptions = []
        new_customer=self.behave_mod.generate_customer()
        end_range = start_of_month + relativedelta(months=+1)
        delta=end_range-start_of_month
        churned = False
        this_month=start_of_month + timedelta(days=randrange(delta.days))
        while not churned:
            next_month=this_month+relativedelta(months=1)
            subscriptions.append( (this_month,next_month) )
            month_count, month_events = new_customer.generate_events(this_month,next_month)
            events.extend(month_events)
            churned=self.util_mod.simulate_churn(month_count) or next_month > self.end_date
            if not churned:
                this_month = next_month
        new_customer.subscriptions=subscriptions
        new_customer.events=events
        return new_customer


    def create_customers_for_month(self,db,month_date,n_to_create):

        for i in range(n_to_create):
            customer = self.simulate_customer(month_date)
            with open(self.tmp_sub_file_name,'w') as tmp_file:
                for s in customer.subscriptions:
                    tmp_file.write("%d,%d,'%s','%s','%s',%f,\\null,\\null,1\n" % \
                        (self.subscription_count,customer.id,self.model_name,s[0],s[1],self.mrr) )
                    self.subscription_count+=1
            with open(self.tmp_event_file_name,'w') as tmp_file:
                for e in customer.events:
                    tmp_file.write("%d,'%s',%d\n" % (customer.id,e[0],e[1]))
            sql = "COPY %s.subscription FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (self.model_name,self.tmp_sub_file_name)
            db.run(sql)
            sql = "COPY %s.event FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (self.model_name,self.tmp_event_file_name)
            db.run(sql)
            print('Simulated customer %d: %d subscription, %d events' %
                  (i,len(customer.subscriptions),len(customer.events) ))

    def cleanup(self,db):
        oldEvent= db.one('select count(*) from %s.event' % self.model_name)
        oldSubs= db.one('select count(*) from %s.subscription' % self.model_name)
        if oldEvent > 0 or oldSubs>0:
            print('TRUNCATING *Events & Subscriptions* in schema -> %s <-  ...' % self.model_name)
            if input("are you sure? (enter %s to proceed) " % self.model_name) == self.model_name:
                if oldEvent > 0:
                    db.run('truncate table %s.event' % self.model_name)
                if oldSubs > 0:
                    db.run('truncate table %s.subscription' % self.model_name)
                return True
            else:
                return False
        else:
            return True

    def run_simulation(self):


        db = Postgres("postgres://%s:%s@localhost/%s" % (
        os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))

        if not self.cleanup(db):
            return

        self.behave_mod.insert_event_types(self.model_name,db)

        print('\nCreating %d initial customers for %s start date' % (self.init_customers,self.start_date))

        self.create_customers_for_month(db,self.start_date,self.init_customers)

        print('Created %d initial customers with %d subscriptions for start date %s' % (self.init_customers,self.subscription_count,str(self.start_date)))


        next_month=self.start_date+relativedelta(months=+1)
        n_to_add = int(ceil( self.init_customers* self.monthly_growth_rate))
        while next_month < self.end_date:
            print('\nCreating %d new customers for month %s:' % (n_to_add,next_month))
            self.create_customers_for_month(db,next_month,n_to_add)
            print('Created %d new customers for month %s, now %d subscriptions\n' % (n_to_add,str(next_month),self.subscription_count))
            next_month=next_month+relativedelta(months=+1)
            n_to_add = int(ceil( n_to_add * (1.0+self.monthly_growth_rate)))


if __name__ == "__main__":

    churn_sim = ChurnSimulation()
    churn_sim.run_simulation()

