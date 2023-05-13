
import pandas as pd
import numpy as np
import os
from math import log, exp
from random import uniform
from shutil import copyfile

from fightchurn.datagen.customer import Customer

class UtilityModel:

    def __init__(self,name):
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

        :param name:
        :param churn_rate: Target churn rate for calibration
        :param behavior_model: The behavior model that this utility function works withy
        '''
        self.name=name
        local_dir = f'{os.path.abspath(os.path.dirname(__file__))}/conf/'
        util_path = local_dir + name+'_utility.csv'
        util_df=pd.read_csv(util_path,index_col=0)
        if 'users' in util_df.index.values:
            assert util_df.index.get_loc('users')==util_df.shape[0]-1, "users should be last in utility list (if included)"
        self.utility_weights=util_df['util']
        self.mrr_utility_cost=self.utility_weights.loc['mrr']
        if self.mrr_utility_cost > 0:
            print(f"*** WARNING: MRR Should have a non-positive utility impact, but found {self.mrr_utility_cost}")
        self.utility_weights = self.utility_weights.drop(['mrr'],axis=0)
        self.behave_names=self.utility_weights.index.values
        transition_path = local_dir + name+'_updownchurn.csv'
        self.transition_df = pd.read_csv(transition_path,index_col=0)

        # Setup in setExpectations,below
        self.behave_means = None
        self.expected_contributions = None
        self.avg_n_user = 0

        save_path = os.path.join(os.getenv('CHURN_OUT_DIR') , self.name )
        os.makedirs(save_path, exist_ok=True)
        copy_path = os.path.join(save_path,  f'{name}_utility.csv')
        copyfile(util_path, copy_path)
        copy_path = os.path.join(save_path,  f'{name}_updownchurn.csv')
        copyfile(transition_path, copy_path)

    def setExpectations(self,bemodDict,model_weights):
        assert sum(model_weights['pcnt'])==1.0, "Model weights should sum to 1.0"
        n_behaviors = len(self.behave_names)
        self.behave_means = np.zeros(n_behaviors)
        for bemod in bemodDict.values():
            underlying_behaviors = Customer.get_underlying_behaviors(bemod.behave_names)
            value_behaviors = {v: Customer.get_behavior_under_value(v,bemod.behave_names) for v in Customer.get_valued_behaviors(bemod.behave_names) }
            assert n_behaviors == len(underlying_behaviors)
            assert all(self.behave_names == underlying_behaviors)
            weight = model_weights.loc[bemod.version,'pcnt']

            # behaviors with values multiply average number times average value
            model_means = bemod.behave_means[underlying_behaviors]
            for vb in value_behaviors.keys():
                model_means.loc[value_behaviors[vb]]=model_means.loc[value_behaviors[vb]]*bemod.behave_means[vb]

            # expected values of non-user behaviors are per-user, so multiply to get the expected total
            if 'users' in bemod.behave_means.index.values:
                model_means[model_means.index!='users'] = model_means[model_means.index!='users']*model_means[model_means.index=='users'].values[0]
                self.avg_n_user = self.avg_n_user + weight* bemod.behave_means['users']
            else:
                self.avg_n_user = self.avg_n_user + weight* 1

            self.behave_means = self.behave_means + weight * np.array(model_means)


        self.expected_contributions = self.behave_means * self.utility_weights.values

    def checkTransitionRates(self, bemodDict, model_weights, plans):
        # Make a single weighted average covariance matrix
        # behave_model_one = bemodDict[next(iter(bemodDict))]
        # behave_var = np.zeros_like(behave_model_one.behave_cov)
        # for bemod in bemodDict.values():
        #     weight = model_weights.loc[bemod.version,'pcnt']
        #     behave_var = behave_var + weight * bemod.behave_cov
        #
        # valued_behaviors = Customer.get_valued_behaviors(behave_model_one.behave_names)
        # if len(valued_behaviors)>0:
        #     # https://www.johndcook.com/blog/2012/10/29/product-of-normal-pdfs/
        #
        # # Volatility of Utility
        # ex_util_vol = np.matmul(np.transpose(self.utility_weights.values), np.matmul(behave_var,self.utility_weights.values))
        # # If users is specified, the covariance does not reflect it
        # ex_util_vol = ex_util_vol * self.avg_n_user
        # ex_util_vol = np.sqrt(np.dot(behave_var, self.utility_weights.values))[0]
        # Temporary Customer
        temp_customer = Customer( pd.DataFrame({'behavior' : self.behave_names, 'monthly_rate': self.behave_means}), satisfaction=1.0)
        temp_customer.mrr = plans['mrr'].mean()
        expected_utility = self.utility_function(self.behave_means, temp_customer)
        print(f'Utility model expected utility={expected_utility}')
        print(self.transition_df)
        print(f'\tExpected churn/down/up prob:')
        util_series = np.linspace(np.round(expected_utility-5*abs(expected_utility)),np.round(expected_utility+5*abs(expected_utility)),20)
        expected_df=pd.DataFrame({'utility':util_series,
                                    'churn' : [self.churn_probability(u) for u in util_series],
                                    'down' : [self.downgrade_probability(u) for u in util_series],
                                    'up' : [self.uprade_probability(u) for u in util_series]})
        print(expected_df)
        save_path = os.path.join(os.getenv('CHURN_OUT_DIR') , self.name )
        os.makedirs(save_path, exist_ok=True)
        expected_df.to_csv(os.path.join(save_path, f'{self.name}_expected_probabilities.csv'))

        if input("okay? (enter y to proceed) ") != 'y':
            exit(0)

    def utility_function(self,event_counts,customer):
        '''
        Utility calculation for a customer:
        1. Take the ratios of the customer's event counts to the mean event counts
        
        :param event_counts:
        :return:
        '''
        contrib_ratios = event_counts / self.behave_means

        if isinstance(customer.satisfaction_propensity, np.ndarray):
            assert customer.satisfaction_propensity.shape == contrib_ratios.shape
            contrib_ratios = contrib_ratios * customer.satisfaction_propensity

        utility_contribs = self.expected_contributions * (1.0 - np.exp(-2.0*contrib_ratios))
        utility = np.sum(utility_contribs)
        utility = utility + customer.mrr* self.mrr_utility_cost * customer.monetary_satisfaction

        if isinstance(customer.satisfaction_propensity,float):
            if customer.satisfaction_propensity != 1.0:
                multiplier = customer.satisfaction_propensity if utility > 0.0  else (1.0/customer.satisfaction_propensity)
            else:
                multiplier = 1.0
            utility *= multiplier

        customer.current_utility = utility
        return utility

    def transition_probility(self,u,trans):
        offset = self.transition_df.loc[trans,'offset']
        scale = self.transition_df.loc[trans,'scale']
        prob=1.0/(1.0 + exp(-1.*scale * u + offset))
        if trans in ['downsell','churn']:
            prob = 1.0 - prob
        return prob


    def churn_probability(self,u):
        churn_prob = self.transition_probility(u,'churn')
        return churn_prob

    def downgrade_probability(self,u):
        down_prob= self.transition_probility(u,'downsell')
        return down_prob


    def uprade_probability(self,u):
        up_prob = self.transition_probility(u,'upsell')
        return up_prob

    def simulate_churn(self,event_counts,customer):
        '''
        Simulates one customer churn, given a set of event counts.  The retention probability is a sigmoidal function
        in the utility, and the churn probability is 100% minus retention. The return value is a binary indicating
        churn or no churn, by comparing a uniform random variable on [0,1] to the churn probability.
        :param event_counts:
        :return:
        '''
        # utility = self.utility_function(event_counts,customer)
        return uniform(0, 1) < self.churn_probability(customer.current_utility)

    def simulate_upgrade_downgrade(self,event_counts,customer,plans, add_ons):
        '''
        Assuming plans are sorted by MRR, an upgrade means higher index
        :param event_counts:
        :param customer:
        :param plans:
        :return:
        '''
        current_plan = np.where(plans.index.values==customer.plan)[0][0]
        # u=self.utility_function(event_counts,customer)
        upgrade_probability = self.uprade_probability(customer.current_utility)
        downgrade_probability = self.downgrade_probability(customer.current_utility)
        # churn_probability = self.churn_probability(u)
        # print(f'u={u}, c={churn_probability}, up={upgrade_probability}, down={downgrade_probability}')

        changed_plan=False
        changed_add_ons=False
        if uniform(0, 1) < upgrade_probability:
            near_limit=None
            if plans.shape[1]>2:
                for limited in plans.columns.values[2:]:
                    current_limit=plans.iloc[current_plan][limited]
                    max_limit=plans[limited].max()
                    customer_rate = customer.get_behavior_rate(limited)
                    if customer_rate>= 0.66* current_limit and max_limit>current_limit:
                        near_limit = limited
                        break

            if near_limit is not None:
                # upgrade to a higher limit plan with the same billing period
                same_period_plans = plans[plans['bill_period']==customer.bill_period]
                # sorting so the customer takes the next higher limit plan
                higher_limit_plans =  same_period_plans[same_period_plans[limited]>current_limit].sort_values(by=limited)
                if len(higher_limit_plans)>0:
                    new_plan_name = higher_limit_plans.index.values[0]
                    customer.set_plan(plans,plan_name=new_plan_name)
                    changed_plan=True
            # if there was no suitable upgrade, try to increase the billing period
            if not changed_plan and 'bill_period' in plans.columns.values:
                # upgrade to a plan with same limits and a longer billing period
                current_period = customer.bill_period
                max_period = plans['bill_period'].max()
                if current_period < max_period:
                    first_limit = plans.columns.values[2]
                    same_limit_plans = plans[plans[first_limit]==customer.limits[first_limit]]
                    # not sorting, the order is random - so customer could go to any higher period plan
                    higher_period_plans =  same_limit_plans[same_limit_plans['bill_period']>customer.bill_period]
                    new_plan_name = higher_period_plans.index.values[0]
                    customer.set_plan(plans,plan_name=new_plan_name)
                    changed_plan=True

        # if they didn't upgrade, check for downgrades
        if not changed_plan and uniform(0, 1) < downgrade_probability:
            # See if any downgrades are available
            if plans.shape[1] > 2:
                first_limit = plans.columns.values[2]
                same_period_plans = plans[plans['bill_period']==customer.bill_period]
                # sorting so the customer takes the next lower limit plan
                lower_limit_plans =  same_period_plans[same_period_plans[first_limit]<customer.limits[first_limit]].sort_values(by=first_limit)
                if len(lower_limit_plans)>0:
                    new_plan_name = lower_limit_plans.index.values[len(lower_limit_plans)-1]
                    customer.set_plan(plans,plan_name=new_plan_name)
                    changed_plan=True
            # If no suitable dowgrade, try to lower the billing period
            if not changed_plan and 'bill_period' in plans.columns.values:
                same_limit_plans = plans[plans[first_limit]==customer.limits[first_limit]]
                # not sorting, the order is random - so customer could go to any lower period plan
                lower_period_plans =  same_limit_plans[same_limit_plans['bill_period']<customer.bill_period]
                if len(lower_period_plans)>0:
                    new_plan_name = lower_period_plans.index.values[len(lower_period_plans)-1]
                    customer.set_plan(plans,plan_name=new_plan_name)
                    changed_plan=True

        # add ons check - same as upgrade probability
        if uniform(0, 1) < upgrade_probability:
            shuffled_add_ons = add_ons.sample(frac=1).reset_index(drop=True)
            for add_on in shuffled_add_ons.iterrows():
                if len(customer.add_ons)>0 and add_on[1]['plan'] in customer.add_ons['plan'].values:
                    continue
                near_limit = False
                for limited in add_on[1].index.values[3:]:
                    customer_rate = customer.get_behavior_rate(limited)
                    if customer_rate > 0.66*customer.limits[limited] and add_on[1].loc[limited]>0:
                        near_limit = True
                        break
                if not near_limit:
                    continue
                if len(customer.add_ons)==0:
                    customer.add_ons=pd.DataFrame([add_on[1]])
                else:
                    customer.add_ons = customer.add_ons.append(add_on[1])
                changed_add_ons=True
                break

        if not changed_plan and not changed_add_ons:
            for add_on in customer.add_ons.iterrows():
                if uniform(0, 1) < downgrade_probability:
                    customer.add_ons = customer.add_ons.drop(customer.add_ons[customer.add_ons['plan']==add_on[1]['plan']].index)
                    changed_add_ons=True
                    break

        if changed_plan or changed_add_ons:
            customer.add_add_ons(plans)