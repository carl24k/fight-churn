
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
from random import randrange
from postgres import Postgres
from math import ceil
import os

from customer import Customer
from behavior import GaussianBehaviorModel
from utility import UtilityModel

model_name='churnsim1'
tmp_sub_file_name='/tmp/%s_tmp_sub.csv' % model_name
tmp_event_file_name='/tmp/%s_tmp_event.csv' % model_name
start_date = date(2019,1,1)
end_date = date(2019,6,1)
init_customers=100
monthly_growth_rate = 0.2
monthly_churn_rate = 0.1
mrr=9.99

db = Postgres("postgres://%s:%s@localhost/%s" % (
os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))

behave_mod=GaussianBehaviorModel(model_name)
util_mod=UtilityModel(model_name,monthly_churn_rate,behave_mod)


def simulate_customer(start_of_month):
    events = []
    subscriptions = []
    new_customer=behave_mod.generate_customer()
    end_range = start_of_month + relativedelta(months=+1)
    delta=end_range-start_of_month
    churned = False
    this_month=start_of_month + timedelta(days=randrange(delta.days))
    while not churned:
        next_month=this_month+relativedelta(months=1)
        subscriptions.append( (this_month,next_month) )
        month_count, month_events = new_customer.generate_events(this_month,next_month)
        events.extend(month_events)
        churned=util_mod.simulate_churn(month_count) or next_month > end_date
        if not churned:
            this_month = next_month
    new_customer.subscriptions=subscriptions
    new_customer.events=events
    return new_customer


def create_customers_for_month(month_date,n_to_create,subscription_count):

    for i in range(n_to_create):
        customer = simulate_customer(month_date)
        with open(tmp_sub_file_name,'w') as tmp_file:
            for s in customer.subscriptions:
                tmp_file.write("%d,%d,'%s','%s','%s',%f,\\null,\\null,1\n" % \
                    (subscription_count,customer.id,model_name,s[0],s[1],mrr) )
                subscription_count+=1
        with open(tmp_event_file_name,'w') as tmp_file:
            for e in customer.events:
                tmp_file.write("%d,'%s',%d\n" % (customer.id,e[0],e[1]))
        sql = "COPY %s.subscription FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (model_name,tmp_sub_file_name)
        db.run(sql)
        sql = "COPY %s.event FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (model_name,tmp_event_file_name)
        db.run(sql)
        print('Simulated customer %d: %d subscription, %d events @ %s' %
              (i,len(customer.subscriptions),len(customer.events),str(datetime.now())) )
    return subscription_count


print('\nCreating %d initial customers for %s start date' % (init_customers,start_date))
subscription_count=0
subscription_count = create_customers_for_month(start_date,init_customers,subscription_count)

print('Created %d initial customers with %d subscriptions for start date %s' % (init_customers,subscription_count,str(start_date)))


next_month=start_date+relativedelta(months=+1)
n_to_add = int(ceil( init_customers* monthly_growth_rate))
while next_month < end_date:
    print('\nCreating %d new customers for month %s:' % (n_to_add,next_month))
    subscription_count = create_customers_for_month(next_month,n_to_add,subscription_count)
    print('Created %d new customers for month %s, now %d subscriptions\n' % (n_to_add,str(next_month),subscription_count))
    next_month=next_month+relativedelta(months=+1)
    n_to_add = int(ceil( n_to_add * (1.0+monthly_growth_rate)))
