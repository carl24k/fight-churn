import pandas as pd
import numpy as np
from listing_5_3_metric_scores import metric_scores

def apply_metric_groups(data_set_path='',save=True):

    score_data = metric_scores(data_set_path,save=False)
    data_2group = score_data.drop('is_churn',axis=1)

    load_mat_df = pd.read_csv(data_set_path.replace('.csv', '_load_mat.csv'), index_col=0)
    load_mat_ndarray = load_mat_df.to_numpy()

    # Make sure the data is in the same column order as the rows of the loading matrix
    ndarray_2group = data_2group[load_mat_df.index.values].to_numpy()
    grouped_ndarray = np.matmul(ndarray_2group, load_mat_ndarray)

    grouped_column_names = ['metric_group_%d' % (d + 1) for d in range(0, load_mat_df.shape[1])]
    churn_data_grouped = pd.DataFrame(grouped_ndarray,columns=grouped_column_names, index=score_data.index)
    churn_data_grouped = churn_data_grouped / churn_data_grouped.std()

    churn_data_grouped['is_churn'] = score_data['is_churn']

    if save:
        save_path = data_set_path.replace('.csv', '_group_scores.csv')
        churn_data_grouped.to_csv(save_path,header=True)
        print('Saved grouped data  to ' + save_path)

    return churn_data_grouped
