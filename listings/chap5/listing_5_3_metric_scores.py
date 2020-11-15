import pandas as pd
import numpy as np
import os

def metric_scores(data_set_path, skew_thresh=4.0):

    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    data_scores = churn_data.copy()
    data_scores.drop('purchase',axis=1)

    stat_path = data_set_path.replace('.csv', '_summarystats.csv')
    assert os.path.isfile(stat_path),'You must running listing 5.2 first to generate stats'
    stats = pd.read_csv(stat_path,index_col=0)
    # stats=stats.drop('purchase')
    skewed_columns_series=(stats['skew']>skew_thresh) & (stats['min'] >= 0)
    skewed_columns=skewed_columns_series[skewed_columns_series]

    for col in skewed_columns.keys():
        data_scores[col]=np.log(1.0+data_scores[col])
        stats.at[col,'mean']=data_scores[col].mean()
        stats.at[col,'std']=data_scores[col].std()


    data_scores=(data_scores-stats['mean'])/stats['std']
    data_scores['purchase']=churn_data['purchase']

    score_save_path=data_set_path.replace('.csv','_scores.csv')
    print('Saving results to %s' % score_save_path)
    data_scores.to_csv(score_save_path,header=True)


    param_df = pd.DataFrame({'skew_score': skewed_columns_series,
                             'fattail_score': [False] * len(stats['mean']),
                             'mean': stats['mean'],
                             'std': stats['std']})
    param_save_path=data_set_path.replace('.csv','_score_params.csv')
    param_df.to_csv(param_save_path,header=True)
    print('Saving params to %s' % param_save_path)

