import pandas as pd
import numpy as np
import os

def reload_churn_data(data_set_path,suffix,listing,is_customer_data):
    data_path = data_set_path.replace('.csv', '_{}.csv'.format(suffix))
    assert os.path.isfile(data_path),'You must run listing {} to save {} first'.format(listing,suffix)
    if is_customer_data:
        churn_data = pd.read_csv(data_path)
        churn_data.set_index(['account_id', 'observation_date'], inplace=True)
    else:
        churn_data = pd.read_csv(data_path, index_col=0)
    return churn_data

def rescore_metrics(data_set_path='', save=True):

    load_mat_df = reload_churn_data(data_set_path,'load_mat','6.4',is_customer_data=False)
    transform_df = reload_churn_data(data_set_path,'score_params','7.5',is_customer_data=False)
    current_data = reload_churn_data(data_set_path,'current','8.2',is_customer_data=True)

    for col in transform_df[transform_df['skew_score']].index.values:
        current_data[col]=np.log(1.0+current_data[col])

    for col in transform_df[transform_df['fattail_score']].index.values:
        current_data[col]=np.log(current_data[col] + np.sqrt(np.power(current_data[col],2) + 1.0) )

    assert set(transform_df.index.values)==set(current_data.columns.values),"Data to re-score does not match transform params"
    current_data=current_data[transform_df.index.values]
    current_data=(current_data-transform_df['mean'])/transform_df['std']

    assert set(load_mat_df.index.values)==set(current_data.columns.values),"Data to re-score does not match load matrix"
    ndarray_2group = current_data[load_mat_df.index.values].to_numpy()
    grouped_ndarray = np.matmul(ndarray_2group, load_mat_df.to_numpy())

    if save:
        score_save_path=data_set_path.replace('.csv','_groupscore.csv')
        np.savetxt(score_save_path,grouped_ndarray)
        print('Saving results to %s' % score_save_path)

    return grouped_ndarray
