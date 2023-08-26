

import numpy as np
import os
import pandas as pd

from shutil import copyfile

from fightchurn.churnsim.customer import Customer

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

    def generate_customer(self,start_of_month, args):
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

class NormalBehaviorModel(BehaviorModel):

    def __init__(self,name,random_seed=None,version='model'):
        '''
        This behavior model uses a mean and (pseudo) covariance matrix to generate customers with event rates.
        The parameters are passed on a csv file that should be located in a `conf` directory adjacent to the code.
        The format of the data file is:
            first column of the data file should be the names and must have the heading 'behavior'
            second column is the mean rates and must have the heading 'mean'
            third column - optional - maximum behavior rates
            the remaining columns should be a pseudo-covariance matrix for the behaviors, so it must be real valued and
            have the right number of columns with column names the same as the rows
        These are loaded using pandas.

        For a detailed explanation see the ChurnSim report, section 3.2.1, "Behavior Model"
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160

        Note that the Gaussian base class is currently deprecated and the Log-Normal version is used instead.
        :param name:
        '''
        self.name=name
        self.version=version
        local_dir = f'{os.path.abspath(os.path.dirname(__file__))}/conf/'
        model_path= local_dir +name + '_' + version + '.csv'
        model=pd.read_csv(model_path)
        model.set_index(['behavior'],inplace=True)
        self.behave_means=model['mean']
        self.behave_maxs = None
        if 'max' in model.columns:
            self.behave_maxs = model['max']
        self.behave_names=model.index.values
        if not all([b in model.columns.values for b in self.behave_names]):
            raise ValueError(f'Covariance columns missing behaviors in rows: {list(set(self.behave_names)-set(model.columns))}')
        self.behave_cov=model[self.behave_names]
        self.min_rate=0.01*self.behave_means.min()
        corr_scale=(np.absolute(self.behave_cov.to_numpy()) <= 1.0).all()
        if random_seed is not None:
            np.random.seed(random_seed)
        if not is_pos_def(self.behave_cov):
            if input("Matrix is not positive semi-definite: Multiply by transpose? (enter Y to proceed)") in ('y','Y'):
                # https://stackoverflow.com/questions/619335/a-simple-algorithm-for-generating-positive-semidefinite-matrices
                self.behave_cov= np.dot(self.behave_cov, self.behave_cov.transpose())
            else:
                exit(0)

        if corr_scale:
            self.scale_correlation_to_covariance()

        # Save to a csv
        save_path = os.path.join(os.getenv('CHURN_OUT_DIR') , self.name )
        os.makedirs(save_path, exist_ok=True)
        copy_path = os.path.join(save_path,  f'{name}_{version}_simulation_model.csv')
        copyfile(model_path, copy_path)

        # For debugging
        # np.savetxt('../conf/'+name+ '_behavior_cov.csv', self.behave_cov,delimiter=',')
        # std_ = np.sqrt(np.diag(self.behave_cov))
        # corr = self.behave_cov / np.outer(std_, std_)
        # np.savetxt('../conf/'+name+ '_behavior_corr.csv', corr,delimiter=',')
        # exit(0)


    def scale_correlation_to_covariance(self):
        # print('Scaling correlation by behavior means...')
        # This seems to give a reasonable amount of variance if the matrix was designed as a set of correlations
        scaling = np.sqrt(self.behave_means.abs() * np.sqrt(self.behave_means.abs()))
        self.behave_cov = np.matmul(self.behave_cov, np.diag(scaling))
        self.behave_cov = np.matmul(np.diag(scaling), self.behave_cov)

    def behave_var(self):
        return np.diagonal(self.behave_cov)

    def generate_customer(self,start_of_month, args):
        '''
        Given a mean and covariance matrix, the event rates for the customer are drawn from the multi-variate
        gaussian distribution.
        :return: a Custoemr object
        '''
        customer_rates=np.random.multivariate_normal(mean=self.behave_means,cov=self.behave_cov)
        customer_rates=customer_rates.clip(min=self.min_rate) # clip : no negative rates!
        new_customer= Customer( pd.DataFrame({'behavior' : self.behave_names, 'monthly_rate': customer_rates}),
                                start_of_month, args)
        # print(customer_rates)
        return new_customer


class LogNormalBehaviorModel(NormalBehaviorModel):

    def __init__(self,name,exp_base, random_seed=None,version=None):
        """
        This is the Log-Normal version of the behavior model

        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - section 3.2.1, "Behavior Model"
        - Section 3.4.2, Product Channels

        :param name:
        :param exp_base:
        :param random_seed:
        :param version:
        """
        self.exp_base = exp_base
        self.log_fun = lambda x: np.log(x) / np.log(self.exp_base)
        self.exp_fun = lambda x: np.power(self.exp_base,x)

        super(LogNormalBehaviorModel, self).__init__(name, random_seed, version)

    def scale_correlation_to_covariance(self):
        self.log_means=self.log_fun(self.behave_means)
        rectified_means =np.array([max(m,0.0) for m in self.log_means])
        # print('Scaling correlation by behavior means...')

        scaling = np.sqrt(rectified_means)
        self.behave_cov = np.matmul(self.behave_cov, np.diag(scaling))
        self.behave_cov = np.matmul(np.diag(scaling), self.behave_cov)

    def behave_var(self):
        return self.exp_fun( np.diagonal(self.behave_cov))

    def generate_customer(self,start_of_month,args):
        '''
        Given a mean and covariance matrix, the event rates for the customer are drawn from the multi-variate
        gaussian distribution.

        For a detailed explanation see the ChurnSim report
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4540160
        - section 3.2.1, "Behavior Model"

        Also ,subtract 0.5 and set min at 0.5 per month, so there can be very low rates despite 0 (1) min in log normal sim
        :return: a Customer object
        '''
        customer_rates=np.random.multivariate_normal(mean=self.log_means,cov=self.behave_cov)
        customer_rates=self.exp_fun(customer_rates)
        customer_rates = np.maximum(customer_rates-0.667,0.333)
        if self.behave_maxs is not None:
            customer_rates = customer_rates.clip(max=self.behave_maxs).to_numpy()
        new_customer= Customer(pd.DataFrame({'behavior' : self.behave_names, 'monthly_rate': customer_rates}),
                               start_of_month=start_of_month,args=args,channel_name=self.version)
        # print(customer_rates)
        return new_customer
