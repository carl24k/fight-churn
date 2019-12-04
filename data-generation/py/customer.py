
from datetime import date, datetime, timedelta,time
from numpy import random
from random import randrange
import numpy as np

class Customer:
    id_counter=0
    def __init__(self,behavior_rates,satisfaction=None):
        '''
        Creates a customer for simulation, given an ndarray of behavior rates, which are converted to daily.
        Each customer also has a unique integer id which will become the account_id in the database, and holds its
        own subscriptions and events.
        :param behavior_rates: ndarray of behavior rates, which are assumed to be PER MONTH
        '''
        self.behave_per_month=behavior_rates
        self.behave_per_day = (1.0/30.0)*self.behave_per_month
        self.id=Customer.id_counter # set the id to the current class variable
        if satisfaction is None:
            self.satisfaction_propensity = np.power(2.0, random.uniform(-0.75, 0.75))
        else:
            self.satisfaction_propensity = satisfaction
        Customer.id_counter+=1 # increment the class variable
        self.subscriptions=[]
        self.events=[]

    def generate_events(self,start_date,end_date):
        '''
        Generate a sequence of events at the customers daily rates.  Each count for an event on a day is droing from
        a poisson distribution with the customers average rate.  If the number is greater than zero, that number of events
        are created as tuples of time stamps and the event index (which is the database type id).  The time of the
        event is randomly set to anything on the 24 hour range.
        :param start_date: datetime.date for start of simulation
        :param end_date: datetime.date for end of simulation
        :return: The total count of each event, the list of all of the event tuples
        '''

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

        self.events.extend(events)

        return counts