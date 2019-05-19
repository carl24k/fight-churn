
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
from random import randrange
from postgres import Postgres
import os

from customer import Customer
from behavior import GaussianBehaviorModel
from utility import UtilityModel

model_name='churnsim1'
tmp_sub_file_name='/tmp/%s_tmp_sub.csv' % model_name
tmp_event_file_name='/tmp/%s_tmp_event.csv' % model_name
start_date = date(2018,1,1)
end_date = date(2019,1,1)
init_customers=100
monthly_growth_rate = 0.06
monthly_churn_rate = 0.05
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

subscription_count=0
for i in range(init_customers):
    customer = simulate_customer(start_date)
    with open(tmp_sub_file_name,'w') as tmp_file:
        for s in customer.subscriptions:
            tmp_file.write("%d,%d,'%s','%s','%s',%f,\\null,\\null,1\n" % \
                (subscription_count,customer.id,model_name,s[0],s[1],mrr) )
            subscription_count+=1
    with open(tmp_event_file_name,'w') as tmp_file:
        for e in customer.events:
            tmp_file.write("%d,'%s',%d\n" % (customer.id,e[0],e[1]))
    print('Simulated customer %d: %d subscription, %d events @ %s' %
          (i,len(customer.subscriptions),len(customer.events),str(datetime.now())) )
    print('Loading to db...')
    sql = "COPY %s.subscription FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (model_name,tmp_sub_file_name)
    db.run(sql)
    sql = "COPY %s.event FROM '%s' USING DELIMITERS ',' WITH NULL AS '\\null'" % (model_name,tmp_event_file_name)
    db.run(sql)

print('Created %d initial customers with %d subscriptions\n' % (init_customers,subscription_count))


