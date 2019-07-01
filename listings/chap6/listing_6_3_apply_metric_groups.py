import pandas as pd
import numpy as np
from listing_5_3_metric_scores import metric_scores

def apply_metric_groups(data_set_path='',save=True):

    score_data = metric_scores(data_set_path)
    group_data = score_data.drop('is_churn',axis=1)

    load_mat_df = pd.read_csv(data_set_path.replace('.csv', '_load_mat.csv'), index_col=0)
    # assert load_mat_df.index.values in group_data.columns.values and \
    #        group_data.columns.values in load_mat_df.index.values, 'Columns of data and load matrix do not match'
    group_data = group_data[load_mat_df.index.values]
    grouped_ndarray = np.matmul(group_data.to_numpy(), load_mat_df.to_numpy())


    grouped_column_names = ['metric_group_%d' % (d + 1) for d in range(0, load_mat_df.shape[1])]
    churn_data_grouped = pd.DataFrame(grouped_ndarray,columns=grouped_column_names, index=score_data.index)
    churn_data_grouped = churn_data_grouped / churn_data_grouped.std()

    churn_data_grouped['is_churn'] = score_data['is_churn']

    if save:
        churn_data_grouped.to_csv(data_set_path.replace('.csv', '_group_scores.csv'),header=True)

    return churn_data_grouped
