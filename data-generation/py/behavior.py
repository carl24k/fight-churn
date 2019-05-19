

import pandas as pd
import numpy as np

from customer import Customer

def is_pos_def(x):
    '''
    https://stackoverflow.com/questions/16266720/find-out-if-matrix-is-positive-definite-with-numpy
    :param x:
    :return:
    '''
    return np.all(np.linalg.eigvals(x) > 0)

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
        if not is_pos_def(self.behave_cov):
            print('Matrix is not positive semi-definite: Multiplying by transpose')
            weighted_cov=np.matmul(self.behave_cov,np.diag(np.sqrt(self.behave_means)))
            # https://stackoverflow.com/questions/619335/a-simple-algorithm-for-generating-positive-semidefinite-matrices
            self.behave_cov= np.dot(weighted_cov, weighted_cov.transpose())




    def generate_customer(self):

        customer_rates=np.random.multivariate_normal(mean=self.behave_means,cov=self.behave_cov)
        customer_rates=customer_rates.clip(min=self.min_rate)
        new_customer= Customer(customer_rates)
        return new_customer