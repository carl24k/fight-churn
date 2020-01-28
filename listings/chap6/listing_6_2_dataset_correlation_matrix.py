import pandas as pd

def dataset_correlation_matrix(data_set_path):

    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    churn_data = churn_data.reindex(sorted(churn_data.columns), axis=1)
    corr = churn_data.corr()

    save_name = data_set_path.replace('.csv', '_correlation_matrix.csv')
    corr.to_csv(save_name)
    print('Saved correlation matrix to ' + save_name)
