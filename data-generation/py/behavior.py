

import pandas as pd
import numpy as np

from customer import Customer

def is_pos_def(x):
    '''
    Quick check of whether the given matrix is positive definite
    https://stackoverflow.com/questions/16266720/find-out-if-matrix-is-positive-definite-with-numpy
    https://stackoverflow.com/questions/42908334/checking-if-a-matrix-is-symmetric-in-numpy
    :param x:
    :return: true/false
    '''
    rtol = 1e-05
    atol = 1e-08
    return np.all(np.linalg.eigvals(x) > 0) and np.allclose(x, x.T, rtol=rtol, atol=atol)

class BehaviorModel:

    def generate_customer(self):
        '''
        This is the main result expected of the behaviora model: produce customers that can be simulated.
        Implemented by sub-classes, so this definition serves as an interface definition.
        :return:
        '''
        raise NotImplementedError('Sub-classes must define generate_customer!')

    def insert_event_types(self,schema_name,db):
        '''
        A second function of the behavior model is to make sure the database is ready to accept the type of events
        that it produces. This does that by scanning the event type table and inserting any events produced by the model
        that are not alraedy in the table.   Insert the event types for a given schema into the database.
        :param schema_name: string name of the schenma
        :param db: postgres.Posrtgres
        :return:
        '''
        for idx,e in enumerate(self.behave_names):
            id = db.one(self.eventIdSql(schema_name, e))
            if id is None:
                db.run("INSERT into %s.event_type VALUES (%d,'%s');" % (schema_name,idx,e) )

    def eventIdSql(self,schema, event_name):
        '''
        SQL to check if an event id is already in the event type table
        :param schema:
        :param event_name:
        :return:
        '''
        return "select event_type_id from %s.event_type where event_type_name='%s'" % (schema, event_name)

class GaussianBehaviorModel(BehaviorModel):

    def __init__(self,name):
        '''
        This behavior model uses a mean and (pseudo) covariance matrix to generate customers with event rates.
        The parameters are passed on a csv file that should be located in a `conf` directory adjacent to the code.
        The format of the data file is:
            first column of the data file should be the names and must have the heading 'behavior'
            second colum is the mean rates and must have the heading 'mean'
            the remaining columns should be a pseudo-covariance matrix for the behaviors, so it must be real valued and
            have the right number of columns with column names the same as the rows
        These are loaded using pandas.
        :param name:
        '''
        self.name=name
        data=pd.read_csv('../conf/'+name+'_behavior.csv')
        data.set_index(['behavior'],inplace=True)
        self.behave_means=data['mean']
        self.behave_names=data.index.values
        self.behave_cov=data[self.behave_names]
        self.min_rate=0.01*self.behave_means.min()
        if not is_pos_def(self.behave_cov):
            print('Matrix is not positive semi-definite: Multiplying by transpose')
            # https://stackoverflow.com/questions/619335/a-simple-algorithm-for-generating-positive-semidefinite-matrices
            self.behave_cov= np.dot(self.behave_cov, self.behave_cov.transpose())
        if all(self.behave_cov.abs() <= 1.0):
            print('Scaling correlation by behavior means...')
            # This seems to give a reasonable amount of variance if the matrix was designed as a set of correlations
            scaling=self.behave_means.abs() * np.sqrt(self.behave_means.abs())
            self.behave_cov=np.matmul(self.behave_cov,np.diag(scaling))

        # For debugging
        # np.savetxt('../conf/'+name+ '_behavior_cov.csv', self.behave_cov,delimiter=',')





    def generate_customer(self):
        '''
        Given a mean and covariance matrix, the event rates for the customer are drawn from the multi-variate
        gaussian distribution.
        :return: a Custoemr object
        '''
        customer_rates=np.random.multivariate_normal(mean=self.behave_means,cov=self.behave_cov)
        customer_rates=customer_rates.clip(min=self.min_rate) # clip : no negative rates!
        new_customer= Customer(customer_rates)
        return new_customer