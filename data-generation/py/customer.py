
from datetime import date, datetime, timedelta,time
from numpy import random
from random import randrange

class Customer:
    id_counter=0
    def __init__(self,behavior_rates):
        self.behave_per_month=behavior_rates
        self.behave_per_day = (1.0/30.0)*self.behave_per_month
        self.id=Customer.id_counter
        Customer.id_counter+=1
        self.subscriptions=[]
        self.events=[]

    def generate_events(self,start_date,end_date):

        delta = end_date - start_date

        events=[]
        counts=[0]*len(self.behave_per_day)
        for i in range(delta.days):
            the_date = start_date + timedelta(days=i)
            for event_idx,rate in  enumerate(self.behave_per_day):
                new_count=random.poisson(rate)
                counts[event_idx] += new_count
                for n in range(0,new_count):
                    event_time=datetime.combine(the_date,time(randrange(24),randrange(60),randrange(60)))
                    new_event=(event_time,event_idx)
                    events.append(new_event )

        return counts, events