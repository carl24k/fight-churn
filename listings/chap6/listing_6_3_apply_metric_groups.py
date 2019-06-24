import pandas as pd
import numpy as np

def apply_metric_groups(data_set_path='',save=True):

    score_save_path = data_set_path.replace('.csv', '_scores.csv')
    churn_data = pd.read_csv(score_save_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    group_data = churn_data.copy()
    group_data = group_data.drop('is_churn',axis=1)

    load_mat_df = pd.read_csv(data_set_path.replace('.csv', '_load_mat.csv'), index_col=0)
    grouped_column_names = ['metric_group_%d' % (d + 1) for d in range(0, load_mat_df.shape[1])]

    grouped_ndarray = np.matmul(group_data.to_numpy(), load_mat_df.to_numpy())

    churn_data_grouped = pd.DataFrame(grouped_ndarray,columns=grouped_column_names, index=churn_data.index)

    churn_data_grouped['is_churn'] = churn_data['is_churn']

    if save:
        churn_data_grouped.to_csv(data_set_path.replace('.csv', '_group_scores.csv'),header=True)

    return churn_data_grouped

