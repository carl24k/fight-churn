import pandas as pd

def ordered_correlation_matrix(data_set_path):

    churn_data = pd.read_csv(data_set_path.replace('.csv','_scores.csv'),index_col=[0,1])

    load_mat_df = pd.read_csv(data_set_path.replace('.csv', '_load_mat.csv'), index_col=0)

    churn_data=churn_data[load_mat_df.index.values]

    corr = churn_data.corr()

    save_name = data_set_path.replace('.csv', '_ordered_correlation_matrix.csv')
    corr.to_csv(save_name)
    print('Saved correlation matrix to ' + save_name)
