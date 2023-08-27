import numpy as np
import os
import pandas as pd
import tempfile

from datetime import  datetime, timedelta,time
from dateutil import relativedelta
from filelock import FileLock
from math import ceil
from numpy import random
from random import randrange, randint


class Customer:
    date_multipliers = {}
    ID_FILE = os.path.join(tempfile.gettempdir(), f'churn_customer_id.txt')
    ID_LOCK_FILE = os.path.join(tempfile.gettempdir(), f'churn_customer_id_lock.txt')

    def __init__(self,behavior_rates,start_of_month,args,channel_name='NA'):
        '''
        Creates a customer for simulation, given an ndarray of behavior rates, which are converted to daily.
        Each customer also has a unique integer id which will become the account_id in the database, and holds its
        own subscriptions and events.

        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.2.1, Behavior Model - basics of the behavior model
        - Section 3.3, Simulation Algorithm - use of the daily rates
        - Section 3.4.1, Day of Week Behavioral Fluctuation
        - Section 3.4.2, Product Channels
        - Section 3.4.3, Customer Satisfiability Coefficient
        - Section 3.4.4, Customer Age
        - Section 3.5.1, Multi-User Accounts
        - Section 3.5.2, Action Values
        - Section 3.5.6, Billing Period
        - Section 3.5.7. Discounts

        :param behavior_rates: ndarray of behavior rates, which are assumed to be PER MONTH
        :param start_of_month: The date of the month the customer starts
        :param args: OmegaConf with the program args
        :param channel_name: string name of the channel this customers behavior was drawn from
        '''
        with FileLock(Customer.ID_LOCK_FILE):
            next_id = 0
            if os.path.exists(Customer.ID_FILE):
                with open(Customer.ID_FILE, 'r') as id_file:
                    next_id = int(id_file.readline())
            self.id=next_id # set the id to the current class variable
            with open(Customer.ID_FILE, 'w') as id_file:
                id_file.write(f'{next_id+1}\n')
            if self.id % 100==0:
                print(f'Simulating customer {self.id}...')

        self.behavior_rates = behavior_rates
        self.behavior_rates['mean_value'] = None
        self.args=args


        for valued_behavior in Customer.get_valued_behaviors(self.behavior_rates['behavior'].values):
            underlying_behavior = Customer.get_behavior_under_value(valued_behavior, self.behavior_rates['behavior'].values)
            uidx= self.behavior_rates['behavior']==underlying_behavior
            vidx= self.behavior_rates['behavior']==valued_behavior
            self.behavior_rates.loc[uidx,'mean_value']= self.behavior_rates.loc[vidx,'monthly_rate'].values[0]
            self.behavior_rates = self.behavior_rates.drop(self.behavior_rates[vidx].index,axis=0)

        if 'users' in behavior_rates['behavior'].values:
            bidx= self.behavior_rates['behavior'] == 'users'
            self.users = max(int( round(self.behavior_rates.loc[bidx,'monthly_rate'])),1)
            self.behavior_rates = self.behavior_rates.drop(self.behavior_rates[bidx].index,axis=0)
        else:
            self.users = None


        self.behavior_rates['daily_rate'] = (1.0/30.0)*self.behavior_rates['monthly_rate']
        self.channel=channel_name

        age_range =self.args.max_age - self.args.min_age
        avg_age = age_range/2.0
        if start_of_month:
            self.age=random.uniform(self.args.min_age,self.args.max_age)
            self.date_of_birth = start_of_month + relativedelta.relativedelta(years=-int(self.age),
                                                                              months=-int( (self.age % 1)*12 ),
                                                                              days=-random.uniform(1,30))
        else:
            self.date_of_birth=None
            self.age = avg_age

        self.age_satisfaction_coef = self.args.age_satisfy * (avg_age - self.age)/age_range
        self.country="NA"
        self.mrr=None
        self.discount=0.0
        self.bill_period=1
        self.max_bill_period=None
        self.base_mrr=None
        self.plan=None
        self.add_ons = pd.DataFrame()
        self.limits= {}

        self.satisfaction_propensity = np.power(self.args.satisfy_base,
                                                random.uniform(-self.args.satisfy_scale, self.args.satisfy_scale) \
                                                + self.age_satisfaction_coef )

        self.subscriptions=[]
        self.events=[]
        self.current_utility = None
        self.utility_contribs = None

    def get_behavior_rate(self,behavior):
        if behavior == 'users':
            customer_rate = self.users
        elif behavior in self.behavior_rates['behavior'].values:
            customer_rate = self.behavior_rates[self.behavior_rates['behavior'] == behavior]['monthly_rate'].values[0]
        else:
            raise ValueError(f'get_behavior_rates UNKNOWN behavior {behavior}')
        return customer_rate

    @staticmethod
    def get_valued_behaviors(behavior_list):
        value_behaviors=[]
        for behave in behavior_list:
            if Customer.get_behavior_under_value(behave, behavior_list) is not None:
                value_behaviors.append(behave)
        return value_behaviors

    @staticmethod
    def get_underlying_behaviors(behavior_list):
        underlying_behaviors=[]
        for behave in behavior_list:
            if Customer.get_behavior_under_value(behave, behavior_list) is None:
                underlying_behaviors.append(behave)
        return underlying_behaviors

    @staticmethod
    def get_behavior_under_value(one_behavior, behavior_list):
        if not one_behavior.endswith('_value'):
            return None
        base_behave=str(one_behavior).replace('_value','')
        if base_behave in behavior_list:
            return base_behave
        else:
            return None

    def pick_initial_plan(self, plans, add_ons, bill_periods=None):
        """
        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.5.3 Product Plans, MRR and Limits
        - Section 3.5.6 Billing Periods

        :param plans: Data frame of plans
        :param add_ons: Data frame of add-ons
        :param bill_periods: List of all the possible billing periods
        :return:
        """

        if bill_periods is not None:
            self.max_bill_period=np.random.choice(bill_periods)
            plans_to_use = plans[plans['bill_period'] <= self.max_bill_period]
        else:
            plans_to_use = plans

        if plans.shape[1] < 3:
            choice_index = np.random.choice(range(len(plans_to_use)))
        else:
            # Customer can pick between plans for which its expected number of users
            # is at least 1/3 the plan limit and at most 3x the plan limit
            eligible_plans = []
            for plan_index in range(0,len(plans_to_use)):
                is_eligible = False
                for limited in plans_to_use.columns.values[2:]:
                    plan_limit = plans_to_use.iloc[plan_index][limited]
                    customer_rate = self.get_behavior_rate(limited)
                    min_rate = 0.33*plan_limit if plan_index >0 else 0 # everyone is eligible_plans for first plan
                    max_rate = 3.0  * plan_limit
                    if min_rate <= customer_rate <= max_rate:
                        is_eligible = True
                        break
                if is_eligible:
                    eligible_plans.append(plan_index)
            assert len(eligible_plans)>0
            if len(eligible_plans)==1:
                choice_index = eligible_plans[0]
            else:
                choice_index = np.random.choice(eligible_plans)


        self.set_plan(plans_to_use,choice_index)
        if len(add_ons)>0:
            for add_on in add_ons.iterrows():
                if random.uniform(0,1) <= add_on[1]['prob']:
                    if len(self.add_ons)==0:
                        self.add_ons=pd.DataFrame([add_on[1]])
                    else:
                        new_add_on_df = pd.DataFrame([add_on[1]])
                        self.add_ons=pd.concat([self.add_ons,new_add_on_df])
        self.add_add_ons(plans_to_use)


    def set_plan(self,plans,plan_idx=None, plan_name=None):
        """
        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.5.3, Product PLans, MRR and Limits
        - Section 3.5.5, Add-on Products
        - Section 3.5.6, Billing Periods

        :param plans: data frame of plans
        :param plan_idx: the plan index to set the plan to
        :param plan_name: a name of the plane to set to
        :return:
        """
        if plan_idx is not None:
            self.plan = plans.index.values[plan_idx]
        else:
            self.plan = plan_name
        # 50% chance of a discount as low as 50%
        if np.random.uniform(0, 1) <= self.args.discount_prob:
            # discounts come in multiples of the min, e.g. 1%, 2%, 5% - not any old value
            self.discount = self.args.min_discount * np.round(np.random.uniform(self.args.min_discount,self.args.max_discount)/0.05)
        else:
            self.discount=0.0
        self.mrr = np.round(plans.loc[self.plan,'mrr']* (1.0-self.discount))
        self.base_mrr = self.mrr
        if 'bill_period' in plans.columns.values:
            self.bill_period = plans.loc[self.plan,'bill_period']
        if plans.shape[1]>2:
            self.limits = {
                behave : plans.loc[self.plan, behave] for behave in plans.columns[2:]
            }

    def add_add_ons(self,plans):
        """
        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.5.3, Product PLans, MRR and Limits
        - Section 3.5.5, Add-on Products

        :param plans: data frame of the plans
        :return:
        """
        # Reset to  base MRR
        self.set_plan(plans,plan_name=self.plan)
        for add_on in self.add_ons.iterrows():
            self.mrr+=add_on[1]['mrr']
            for limited in self.add_ons.columns[3:]:
                if limited in self.limits:
                    self.limits[limited]+= add_on[1][limited]
                else:
                    raise ValueError(f'Add on raises a limit {limited} that was not found')


    @staticmethod
    def get_min_max_dow_scale(scale_param):
        """
        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.4.1, Day of Week Behavioral Fluctuation and equation 6

        :param scale_param: Scaling parameter for the day
        :return:
        """
        assert -1.0 <= scale_param < 1.0
        if scale_param > 0:
            min_scale = 1 - 0.1 * scale_param
            max_scale = 1 + scale_param
        else:
            min_scale = 1 + scale_param
            max_scale = 1  - 0.1 * scale_param
        return min_scale, max_scale


    @staticmethod
    def get_day_multiplier(the_date,args):
        """
        Increasing/Decreasing behavior based on the day of the week. Stores one multiplier to be
        used by all customers, the first time a day is encountered.

        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.4.1, Day of Week Behavioral Fluctuation

        :param the_date:
        :param args:
        :return:
        """
        # Set a multiplier for this date
        if the_date not in Customer.date_multipliers:
            if the_date.weekday() >= 4:  # Friday - Sun
                min_scale, max_scale = Customer.get_min_max_dow_scale(args.weekend_scale)
            else:  # Monday-Thursday
                min_scale, max_scale = Customer.get_min_max_dow_scale(args.weekday_scale)
            multiplier = random.uniform(min_scale, max_scale)
            Customer.date_multipliers[the_date] = multiplier
        return Customer.date_multipliers[the_date]


    def generate_events(self,start_date,end_date):
        '''
        Generate a sequence of events at the customers daily rates.  Each count for an event on a day is droing from
        a poisson distribution with the customers average rate.  If the number is greater than zero, that number of events
        are created as tuples of time stamps and the event index (which is the database type id).  The time of the
        event is randomly set to anything on the 24 hour range.

        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.2.1, Behavior Model
        - Section 3.4.1, Day of Week Behavioral Fluctuation
        - Section 3.5.1, Multi-User Accounts
        - Section 3.5.2, Action Values
        - Section 3.5.3, Product Plans, MRR and Limits (specifically the explanation of action limits)

        :param start_date: datetime.date for start of simulation
        :param end_date: datetime.date for end of simulation
        :return: The total count of each event, the list of all of the event tuples
        '''

        delta = end_date - start_date

        events=[]

        if self.users is None:
            counts=[0]*len(self.behavior_rates)
        else:
            counts=[0]*(len(self.behavior_rates)+1) # Plus one for number of users
        limit_counts = {b : 0 for b in self.limits.keys()}
        for i in range(delta.days):
            the_date = start_date + timedelta(days=i)
            dow_multiplier = Customer.get_day_multiplier(the_date,self.args)
            if self.users is None:
                todays_users = 1
            else:
                todays_users = int(round(dow_multiplier*random.poisson(self.users)))
                if 'users' in self.limits:
                    todays_users = min(todays_users,self.limits['users'])

            for row in  self.behavior_rates.iterrows():
                rate = row[1]['daily_rate']
                behavior_name = row[1]['behavior']
                new_count= int(round(dow_multiplier*random.poisson(rate) * todays_users))
                if behavior_name in self.limits:
                    # print(new_count, self.limits, limit_counts)
                    new_count = min(new_count, self.limits[behavior_name]-limit_counts[behavior_name])
                    limit_counts[behavior_name]=limit_counts[behavior_name]+new_count

                for n in range(0,new_count):
                    event_time=datetime.combine(the_date,time(randrange(24),randrange(60),randrange(60)))
                    user_id = 0
                    if self.users is not None:
                        user_id = randint(0, todays_users-1)
                    if row[1]['mean_value'] is not None:
                        event_value = round(np.exp(np.random.normal(np.log(row[1]['mean_value']) )),2)
                        counts[row[0]] += event_value
                    else:
                        event_value = None
                        counts[row[0]] += 1
                    new_event=(event_time, row[0], user_id, event_value)
                    events.append(new_event )

            if self.users is not None:
                counts[-1] += todays_users

        if self.users is not None:
            counts[-1] = int(ceil( counts[-1]/delta.days)) # user count is returned as average, not total

        self.events.extend(events)

        return counts