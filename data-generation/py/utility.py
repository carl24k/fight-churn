
import pandas as pd
import numpy as np
from math import log, exp
from random import uniform

class UtilityModel:

    def __init__(self,name,churn_rate,behavior_model):
        self.name=name
        self.churn_rate = churn_rate
        data=pd.read_csv('../conf/'+name+'_utility.csv')
        data.set_index(['behavior'],inplace=True)
        self.linear_utility=data['util']
        self.behave_names=data.index.values
        self.utility_interactions=data[self.behave_names]

        # pick the constant so the mean behavior has the target churn rate
        expected_utility=self.utility_function(behavior_model.behave_means)
        r=1.0-self.churn_rate
        self.kappa=-log(1.0/r-1.0)/expected_utility

    def utility_function(self,behavior):
        # ToDo: add interaction term
        utility= np.dot(behavior,self.linear_utility)
        return utility

    def simulate_churn(self,event_counts):
        u=self.utility_function(event_counts)
        churn_prob=1.0-1.0/(1.0+exp(-self.kappa*u))
        return uniform(0, 1) < churn_prob