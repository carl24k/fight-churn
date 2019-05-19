

import pandas as pd
import numpy as np

from customer import Customer


class BehaviorModel:

    def generate_customer(self):
        raise NotImplementedError('Sub-classes must define generate_customer!')

    def insert_event_types(self,schema_name,db):
        for idx,e in enumerate(self.behave_names):
            db.run("INSERT into %s.event_type VALUES (%d,'%s');" % (schema_name,idx,e) )

class GaussianBehaviorModel(BehaviorModel):

    def __init__(self,name):
        self.name=name
        data=pd.read_csv('../conf/'+name+'_behavior.csv')
        data.set_index(['behavior'],inplace=True)
        self.behave_means=data['mean']
        self.behave_names=data.index.values
        self.behave_cov=data[self.behave_names]
        self.min_rate=0.01*self.behave_means.min()

    def generate_customer(self):

        customer_rates=np.random.multivariate_normal(mean=self.behave_means,cov=self.behave_cov)
        customer_rates=customer_rates.clip(min=self.min_rate)
        new_customer= Customer(customer_rates)
        return new_customer