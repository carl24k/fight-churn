import pandas as pd
import os
from fightchurn.listings.chap7.listing_7_5_fat_tail_scores import transform_fattail_columns, transform_skew_columns

def clip_hi_cols(data, hi_vals):
    for col in hi_vals.index.values:
        data.loc[data[col] > hi_vals[col],col] = hi_vals[col]

def clip_lo_cols(data, lo_vals):
    for col in lo_vals.index.values:
        data.loc[data[col] < lo_vals[col],col] = lo_vals[col]

def clipped_scores(data_set_path,skew_thresh=4.0):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    data_scores = churn_data.copy()
    data_scores.drop('is_churn',axis=1,inplace=True)

    stat_path = data_set_path.replace('.csv', '_summarystats.csv')
    assert os.path.isfile(stat_path),'You must running listing 5.2 first to generate stats'
    stats = pd.read_csv(stat_path,index_col=0)
    stats.drop('is_churn',inplace=True)

    clip_hi_cols(data_scores, stats['99pct'])
    clip_lo_cols(data_scores, stats['1pct'])

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
