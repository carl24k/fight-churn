
from datetime import date, datetime, timedelta,time
from dateutil import relativedelta
from numpy import random
from random import randrange
import numpy as np



class Customer:
    id_counter=0
    MIN_AGE = 12.0
    MAX_AGE = 82.0
    AGE_RANGE = MAX_AGE - MIN_AGE
    AVG_AGE = (MAX_AGE + MIN_AGE) / 2.0
    date_multipliers = {}

    def __init__(self,behavior_rates,satisfaction=None,channel_name='NA',start_of_month=None,country=None):
        '''
        Creates a customer for simulation, given an ndarray of behavior rates, which are converted to daily.
        Each customer also has a unique integer id which will become the account_id in the database, and holds its
        own subscriptions and events.
        :param behavior_rates: ndarray of behavior rates, which are assumed to be PER MONTH
        '''
        self.id=Customer.id_counter # set the id to the current class variable
        Customer.id_counter+=1 # increment the class variable

        self.behave_per_month=behavior_rates
        self.behave_per_day = (1.0/30.0)*self.behave_per_month
        self.channel=channel_name

        if start_of_month:
            self.age=random.uniform(Customer.MIN_AGE,Customer.MAX_AGE)
            self.date_of_birth = start_of_month + relativedelta.relativedelta(years=-int(self.age),
                                                                              months=-int( (self.age % 1)*12 ),
                                                                              days=-random.uniform(1,30))
        else:
            self.date_of_birth=None

        self.country=country

        if satisfaction is None:
            age_contrib = 0.5* (Customer.AVG_AGE - self.age)/Customer.AGE_RANGE
            self.satisfaction_propensity = np.power(2.0, random.uniform(-1.5, 1.5) + age_contrib)
        else:
            self.satisfaction_propensity = satisfaction
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
            if the_date in Customer.date_multipliers:
                multiplier = Customer.date_multipliers[the_date]
            else:
                if the_date.weekday() >= 4:
                    multiplier = random.uniform(1.00,1.2)
                else:
                    multiplier = random.uniform(0.825,1.025)
                Customer.date_multipliers[the_date]=multiplier
            for event_idx,rate in  enumerate(self.behave_per_day):
                new_count= int(round(multiplier*random.poisson(rate)))
                counts[event_idx] += new_count
                for n in range(0,new_count):
                    event_time=datetime.combine(the_date,time(randrange(24),randrange(60),randrange(60)))
                    new_event=(event_time,event_idx)
                    events.append(new_event )

        self.events.extend(events)

        return counts