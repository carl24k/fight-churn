import pandas as pd
import numpy as np
import os

def fat_tail_scores(data_set_path='',skew_thresh=4.0,save=True,**kwargs):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    data_scores = churn_data.copy()
    data_scores.drop('is_churn',axis=1)

    stat_path = data_set_path.replace('.csv', '_summarystats.csv')
    assert os.path.isfile(stat_path),'You must running listing 5.2 first to generate stats'
    stats = pd.read_csv(stat_path,index_col=0)
    stats.drop('is_churn',inplace=True)

    skewed_columns=(stats['skew']>skew_thresh) & (stats['min'] >= 0)
    fattail_columns=(stats['skew']>skew_thresh) & (stats['min'] < 0)

    for col in skewed_columns[skewed_columns].keys():
        data_scores[col]=np.log(1.0+data_scores[col])

    for col in fattail_columns[fattail_columns].keys():
        data_scores[col]=np.log(data_scores[col] + np.sqrt(np.power(data_scores[col],2) + 1.0) )

    transform_df=pd.DataFrame({'skew_score':skewed_columns,
                               'fattail_score':fattail_columns,
                               'mean' : data_scores.mean(),
                               'std' : data_scores.std()})
    data_scores=(data_scores-transform_df['mean'])/transform_df['std']
    data_scores['is_churn']=churn_data['is_churn']
    transform_df.drop('is_churn',inplace=True)

    if save:
        score_save_path=data_set_path.replace('.csv','_scores.csv')
        data_scores.to_csv(score_save_path,header=True)
        print('Saving results to %s' % score_save_path)
        param_save_path=data_set_path.replace('.csv','_score_params.csv')
        transform_df.to_csv(param_save_path,header=True)
        print('Saving params to %s' % param_save_path)

    return data_scores
