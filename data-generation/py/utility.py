
import pandas as pd
import numpy as np
from math import log, exp
from random import uniform

class UtilityModel:

    def __init__(self,name,churn_rate,behavior_model):
        '''
        This class calculates the churn probability for a customer based on their event counts.  Its called a "Utility
        Model" to mean utility in the economic sense: How much a good or service to satisfies one or more needs or
        wants of a consumer. So how likely the customer is to churn depends on how much utility they get, which is
        based on how many events they have from the behavior model.

        The parameters of the utility model are loaded from a file.  The current implementation loads a file with the
        same form as the behavior model: a vector and a matrix.  The number of these must match the number of
        behaviors in the behavior model. The vector is for calculating multiplicative utility: Each element is multiplied
        by the number of events to get the model utility from those behaviors. The matrix is unused as of this time,
        but the idea was that a second term could be added with the matrix defining utility interactions between the
        behaviors. The utility is calculated in the function `utility_function`

        The churn probability is a sigmoidal function based on utility - see the function `simulate_churn`.

        The model also takes a churn rate as a parameter. The model is calibrated by configuring the slope term of the
        churn probability sigma, which is the class variable `kappa`, so that if a customer has the average behaviors
        (taken from the behavior model means) they will have the target churn rate.  This doesn't guarantee that the
        simulation will have the average churn rate, but it seems to work well enough.

        :param name:
        :param churn_rate: Target churn rate for calibration
        :param behavior_model: The behavior model that this utility function works withy
        '''
        self.name=name
        self.churn_rate = churn_rate
        data=pd.read_csv('../conf/'+name+'_model.csv')
        data.set_index(['behavior'],inplace=True)
        self.linear_utility=data['util']
        self.behave_names=data.index.values
        assert len(self.behave_names)==len(behavior_model.behave_names)
        assert all(self.behave_names == behavior_model.behave_names)
        self.utility_interactions=data[self.behave_names]
        self.behave_means = behavior_model.behave_means
        self.behave_var = behavior_model.behave_var()
        self.fat_tail_fudge = 1.0
        self.util_clip = None
        self.scaled_means = self.fat_tail_fudge*self.behave_means
        self.scaled_vars = self.fat_tail_fudge * self.behave_var
        self.offset_fudge = 0.0

        # pick the constant so the mean behavior has the target churn rate
        self.expected_contributions = self.behave_means*self.linear_utility
        self.expected_utility=self.utility_function(self.scaled_means)
        self.ex_util_vol= np.sqrt( np.dot(self.scaled_vars,self.linear_utility))
        assert self.expected_utility > 0, "Print model requires utility >0, instead expected utility is %f" % self.expected_utility
        r=1.0-self.churn_rate
        self.kappa = -1.0/self.ex_util_vol
        self.offset=log(1.0/r-1.0) -self.kappa*self.expected_utility
        print('Churn={}, Retention={}, offset offset = {} [log(1.0/r-1.0) ]'.format(self.churn_rate,r,log(1.0/r-1.0) ))
        print('Utility model expected util={}, util_vol={}'.format(self.expected_utility,self.ex_util_vol))
        print('\tKappa={}, Offset={}'.format(self.kappa, self.offset))
        expected_churn_prob = self.churn_probability(self.scaled_means)
        print('\tExpected churn prob={}'.format(expected_churn_prob))
        expected_unscaled_prob = self.churn_probability(self.behave_means)
        print('\tMedian churn prob={}'.format(expected_unscaled_prob))
        # exit(0)

    def utility_function(self,behavior):
        '''
        Given a vector of behavior counts, calculate the model for customer utility.  Right now its just a dot
        product and doesn't use the matrix.  That can be added in the future to make more complex simulations.
        :param behavior:
        :return:
        '''

        contrib_ratios = behavior / self.behave_means
        utility_contribs = self.expected_contributions * (1.0 - np.exp(-2.0*contrib_ratios))
        utility = np.sum(utility_contribs)

        return utility

    def churn_probability(self,event_counts):

        u=self.utility_function(event_counts)
        churn_prob=1.0-1.0/(1.0+exp(self.kappa*u + self.offset))
        return churn_prob

    def simulate_churn(self,event_counts):
        '''
        Simulates one customer churn, given a set of event counts.  The retention probability is a sigmoidal function
        in the utility, and the churn probability is 100% minus retention. The return value is a binary indicating
        churn or no churn, by comparing a uniform random variable on [0,1] to the churn probability.
        :param event_counts:
        :return:
        '''
        return uniform(0, 1) < self.churn_probability(event_counts)
