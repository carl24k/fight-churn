import pandas as pd

def dataset_correlation_matrix(data_set_path='',save=True):

    churn_data = pd.read_csv(data_set_path,index_col=[0,1])

    corr = churn_data.corr()

    if save:
        save_name = data_set_path.replace('.csv', '_correlation_matrix.csv')
        corr.to_csv(save_name)
        print('Saved correlation matrix to ' + save_name)
