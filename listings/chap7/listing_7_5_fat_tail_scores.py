import pandas as pd
import numpy as np
import os

def transform_skew_columns(data,skew_col_names):
    for col in skew_col_names:
        data[col] = np.log(1.0+data[col])

def transform_fattail_columns(data,fattail_col_names):
    for col in fattail_col_names:
        data[col] = np.log(data[col] + np.sqrt(np.power(data[col],2) + 1.0))


def fat_tail_scores(data_set_path,skew_thresh=4.0,**kwargs):

    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    data_scores = churn_data.copy()
    data_scores.drop('is_churn',inplace=True,axis=1)

    stat_path = data_set_path.replace('.csv', '_summarystats.csv')
    assert os.path.isfile(stat_path),'You must running listing 5.2 first to generate stats'
    stats = pd.read_csv(stat_path,index_col=0)
    stats.drop('is_churn',inplace=True)

    skewed_columns=(stats['skew']>skew_thresh) & (stats['min'] >= 0)
    transform_skew_columns(data_scores,skewed_columns[skewed_columns].keys())

    fattail_columns=(stats['skew']>skew_thresh) & (stats['min'] < 0)
    transform_fattail_columns(data_scores,fattail_columns[fattail_columns].keys())

    mean_vals = data_scores.mean()
    std_vals = data_scores.std()
    data_scores=(data_scores-mean_vals)/std_vals

    data_scores['is_churn']=churn_data['is_churn']


    score_save_path=data_set_path.replace('.csv','_scores.csv')
    data_scores.to_csv(score_save_path,header=True)
    print('Saving results to %s' % score_save_path)

    param_df = pd.DataFrame({'skew_score': skewed_columns,
                             'fattail_score': fattail_columns,
                             'mean': mean_vals,
                             'std': std_vals})
    param_save_path=data_set_path.replace('.csv','_score_params.csv')
    param_df.to_csv(param_save_path,header=True)
    print('Saving params to %s' % param_save_path)
