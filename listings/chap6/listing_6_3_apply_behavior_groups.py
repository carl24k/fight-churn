import pandas as pd

def dataset_correlation_matrix(data_set_path='',save_path='./'):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)

    corr = churn_data.corr()

    save_name = save_path + '/correlation_matrix.csv'
    corr.to_csv(save_name)
    print('Saved correlation matrix to' + save_name)
