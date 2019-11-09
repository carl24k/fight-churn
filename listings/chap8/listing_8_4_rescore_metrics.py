import pandas as pd
import numpy as np
import os

def reload_churn_data(data_set_path,suffix,listing,is_customer_data):
    data_path = data_set_path.replace('.csv', '_{}.csv'.format(suffix))
    assert os.path.isfile(data_path),'You must run listing {} to save {} first'.format(listing,suffix)
    ic = [0,1] if is_customer_data else 0
    churn_data = pd.read_csv(data_path, index_col=ic)
    return churn_data

def rescore_metrics(data_set_path='', save=True):

    load_mat_df = reload_churn_data(data_set_path,'load_mat','6.4',is_customer_data=False)
    score_df = reload_churn_data(data_set_path,'score_params','7.5',is_customer_data=False)
    current_data = reload_churn_data(data_set_path,'current','8.2',is_customer_data=True)

    for col in score_df[score_df['skew_score']].index.values:
        current_data[col]=np.log(1.0+current_data[col])

    for col in score_df[score_df['fattail_score']].index.values:
        current_data[col]=np.log(current_data[col] + np.sqrt(np.power(current_data[col],2) + 1.0) )

    assert set(score_df.index.values)==set(current_data.columns.values),"Data to re-score does not match transform params"
    current_data=current_data[score_df.index.values]
    scaled_data=(current_data-score_df['mean'])/score_df['std']

    assert set(load_mat_df.index.values)==set(current_data.columns.values),"Data to re-score does not match load matrix"
    scaled_data = scaled_data[load_mat_df.index.values]
    ndarray_2group = scaled_data.to_numpy()
    grouped_ndarray = np.matmul(ndarray_2group, load_mat_df.to_numpy())

    grouped_column_names = ['metric_group_%d' % (d + 1) for d in range(0, load_mat_df.shape[1])]
    current_data_grouped = pd.DataFrame(grouped_ndarray,columns=grouped_column_names, index=current_data.index)

    if save:
        score_save_path=data_set_path.replace('.csv','_current_groupscore.csv')
        current_data_grouped.to_csv(score_save_path,header=True)
        print('Saving results to %s' % score_save_path)

    return current_data_grouped
