import pandas as pd
import numpy as np
import os

def apply_metric_groups(data_set_path='',save=True):

    score_save_path=data_set_path.replace('.csv','_scores.csv')
    assert os.path.isfile(score_save_path),'You must run listing 5.3 or 7.5 to save metric scores first'
    score_data = pd.read_csv(score_save_path,index_col=0)
    data_2group = score_data.drop('is_churn',axis=1)

    load_mat_path = data_set_path.replace('.csv', '_load_mat.csv')
    assert os.path.isfile(load_mat_path),'You must run listing 6.4 to save a loading matrix first'
    load_mat_df = pd.read_csv(load_mat_path, index_col=0)
    load_mat_ndarray = load_mat_df.to_numpy()

    # Make sure the data is in the same column order as the rows of the loading matrix
    ndarray_2group = data_2group[load_mat_df.index.values].to_numpy()
    grouped_ndarray = np.matmul(ndarray_2group, load_mat_ndarray)

    grouped_column_names = ['metric_group_%d' % (d + 1) for d in range(0, load_mat_df.shape[1])]
    churn_data_grouped = pd.DataFrame(grouped_ndarray,columns=grouped_column_names, index=score_data.index)
    group_std = churn_data_grouped.std()
    churn_data_grouped = churn_data_grouped / group_std
    group_std_df = pd.DataFrame({'group':grouped_column_names,'std':group_std})

    churn_data_grouped['is_churn'] = score_data['is_churn']

    if save:
        save_path = data_set_path.replace('.csv', '_groupscore.csv')
        churn_data_grouped.to_csv(save_path,header=True)
        print('Saved grouped data  to ' + save_path)
        save_path = data_set_path.replace('.csv', '_groupstd.csv')
        group_std_df.to_csv(save_path,header=True)
        print('Saved group standard deviations to ' + save_path)

    return churn_data_grouped
