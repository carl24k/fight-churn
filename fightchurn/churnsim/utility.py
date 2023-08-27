import numpy as np
import os
import pandas as pd

from math import  exp
from omegaconf import OmegaConf
from random import uniform

from fightchurn.churnsim.customer import Customer

class UtilityModel:

    def __init__(self,name, args):
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
        self.args = args
        self.contrib_scale =self.args.util_contrib_scale
        self.util_df = pd.DataFrame([list(args.utility.keys()),list(args.utility.values())]).transpose().set_index(0)
        self.util_df.columns=['util']
        self.util_df=self.util_df.astype({'util':float})
        if 'users' in self.util_df.index.values:
            assert self.util_df.index.get_loc('users')==self.util_df.shape[0]-1, "users should be last in utility list (if included)"

        self.utility_weights=self.util_df['util']
        self.mrr_utility_cost=self.utility_weights.loc['mrr']
        if self.mrr_utility_cost > 0:
            print(f"*** WARNING: MRR Should have a non-positive utility impact, but found {self.mrr_utility_cost}")
        self.utility_weights = self.utility_weights.drop(['mrr'],axis=0)
        self.behave_names=self.utility_weights.index.values
        self.transition_df = pd.json_normalize(OmegaConf.to_container(self.args.transition).values(),max_level=1)
        self.transition_df.index = list(self.args.transition.keys())

        # Setup in setExpectations,below
        self.behave_means = None
        self.expected_contributions = None
        self.avg_n_user = 0

        save_path = os.path.join(os.getenv('CHURN_OUT_DIR') , self.name )
        os.makedirs(save_path, exist_ok=True)
        copy_path = os.path.join(save_path,  f'{name}_utility.csv')
        self.util_df.to_csv(copy_path)
        copy_path = os.path.join(save_path,  f'{name}_updownchurn.csv')
        self.transition_df.to_csv(copy_path)

    def setExpectations(self, chan_mod_dict, model_weights):
        """
        Calculates the average utility contribution from each behavior, for use in the utility function.
        For a detailed explanation see  the ChurnSim report:
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.2.2, Utility Model
        - Section 3.4.2, Product Channels

        :param chan_mod_dict: dictionary from channel name to the associated behavior model
        :param model_weights: probability for each channel to be chosen
        :return:
        """
        assert sum(model_weights.values())==1.0, "Model weights should sum to 1.0"
        n_behaviors = len(self.behave_names)
        self.behave_means = np.zeros(n_behaviors)
        for bemod in chan_mod_dict.values():
            underlying_behaviors = Customer.get_underlying_behaviors(bemod.behave_names)
            value_behaviors = {v: Customer.get_behavior_under_value(v,bemod.behave_names) for v in Customer.get_valued_behaviors(bemod.behave_names) }
            assert n_behaviors == len(underlying_behaviors)
            assert all(self.behave_names == underlying_behaviors)
            weight = model_weights[bemod.version]

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


    def utility_function(self,event_counts,customer):
        '''
        Utility calculation for a customer:
        1. Take the ratios of the customer's event counts to the mean event counts
        2. Apply an exponential growth function modeling hedonic adaptation
        3. Add the term for MRR
        4. Apply customer satisfaction propensity


        For a detailed explanation see the ChurnSim report:
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.2.2, Utility Model
        - Section 3.4.3, Customer Satisfiability Coefficient
        - Section 3.5.3, Product Plans, MRR
        
        :param event_counts:
        :return:
        '''
        contrib_ratios = event_counts / self.behave_means
        utility_contribs = self.expected_contributions * (1.0 - np.exp(-self.contrib_scale*contrib_ratios))
        mrr_utility = customer.mrr* self.mrr_utility_cost
        if customer.discount > 0:
            # utility due to getting a discount: -1 so that with mrr_utility_cost this is a positive contribution
            mrr_utility += -1* customer.mrr* self.mrr_utility_cost * customer.discount * self.args.discount_satisfy
        utility_contribs =  np.append(utility_contribs,mrr_utility)
        utility = np.sum(utility_contribs)

        if customer.satisfaction_propensity != 1.0:
            multiplier = customer.satisfaction_propensity if utility > 0.0  else (1.0/customer.satisfaction_propensity)
        else:
            multiplier = 1.0
        utility *= multiplier

        customer.current_utility = utility
        customer.utility_contribs = utility_contribs
        return utility

    def transition_probility(self,u,trans):
        '''
        Transition probability function for upsell, downsell and churn.
        For a detailed explanation see the ChurnSim report:
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.2.3, Churn Model
        - Section 3.5.4, Upgrade & Downgrade

        :param u: The utility value
        :param trans: Which transition (string)
        :return: The probability
        '''
        offset = self.transition_df.loc[trans,'offset']
        scale = self.transition_df.loc[trans,'scale']
        # Clip exponent to prevent overflow errors in extreme cases
        prob=1.0/(1.0 + exp( np.clip(-1.*scale * u + offset, -40.0, 40.0)))
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
        return uniform(0, 1) < self.churn_probability(customer.current_utility)

    def simulate_upgrade_downgrade(self,event_counts,customer,plans, add_ons):
        '''
        Determine one customer's upgrade, downgrade, changes in add-ons and changes in billing period.
        For a detailed explanation see the ChurnSim report:
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - Section 3.5.4, Upgrade & Downgrade
        - Section 3.5.5, Add-on Products
        - Section 3.5.6, Billing Periods

        :param event_counts:
        :param customer:
        :param plans:
        :return:
        '''
        current_plan = np.where(plans.index.values==customer.plan)[0][0]
        upgrade_probability = self.uprade_probability(customer.current_utility)
        downgrade_probability = self.downgrade_probability(customer.current_utility)

        changed_plan=False
        changed_add_ons=False
        changed_bill_period=False
        if uniform(0, 1) < upgrade_probability:
            near_limit=None
            if plans.shape[1]>2:
                for limited in plans.columns.values[2:]:
                    current_limit=plans.iloc[current_plan][limited]
                    max_limit=plans[limited].max()
                    customer_rate = customer.get_behavior_rate(limited)
                    if customer_rate>= 0.5* current_limit and max_limit>current_limit:
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
                max_period_avail = plans['bill_period'].max()
                if current_period < max_period_avail and current_period < customer.max_bill_period:
                    first_limit = plans.columns.values[2]
                    same_limit_plans = plans[plans[first_limit]==customer.limits[first_limit]]
                    # the order is random - so customer could go to any higher period plan
                    higher_period_plans =  same_limit_plans[same_limit_plans['bill_period']>customer.bill_period].sample(frac=1)
                    new_plan_name = higher_period_plans.index.values[0]
                    customer.set_plan(plans,plan_name=new_plan_name)
                    changed_bill_period=True

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
                # the order is random - so customer could go to any lower period plan
                lower_period_plans =  same_limit_plans[same_limit_plans['bill_period']<customer.bill_period].sample(frac=1)
                if len(lower_period_plans)>0:
                    new_plan_name = lower_period_plans.index.values[len(lower_period_plans)-1]
                    customer.set_plan(plans,plan_name=new_plan_name)
                    changed_bill_period=True

        # add ons check - same as upgrade probability
        if uniform(0, 1) < upgrade_probability:
            shuffled_add_ons = add_ons.sample(frac=1).reset_index(drop=True)
            for add_on in shuffled_add_ons.iterrows():
                if len(customer.add_ons)>0 and add_on[1]['plan'] in customer.add_ons['plan'].values:
                    continue
                near_limit = False
                for limited in add_on[1].index.values[3:]:
                    customer_rate = customer.get_behavior_rate(limited)
                    if customer_rate > 0.5*customer.limits[limited] and add_on[1].loc[limited]>0:
                        near_limit = True
                        break
                if not near_limit:
                    continue
                if len(customer.add_ons)==0:
                    customer.add_ons=pd.DataFrame([add_on[1]])
                else:
                    add_on_df = pd.DataFrame([add_on[1]])
                    customer.add_ons = pd.concat([customer.add_ons,add_on_df])
                changed_add_ons=True
                break

        if not changed_add_ons and uniform(0, 1) < downgrade_probability:
            for add_on in customer.add_ons.iterrows():
                customer.add_ons = customer.add_ons.drop(customer.add_ons[customer.add_ons['plan']==add_on[1]['plan']].index)
                changed_add_ons=True
                break

        if changed_plan or changed_add_ons:
            customer.add_add_ons(plans)

        return changed_bill_period
