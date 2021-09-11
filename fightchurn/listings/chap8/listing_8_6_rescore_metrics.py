import pandas as pd
import numpy as np
from fightchurn.listings.chap7.listing_7_5_fat_tail_scores import transform_fattail_columns, transform_skew_columns
from fightchurn.listings.chap8.listing_8_4_rescore_metrics import reload_churn_data

def clip_hi_cols(data, hi_vals):
    for col in hi_vals.index.values:
        data.loc[data[col] > hi_vals[col],col] = hi_vals[col]

def clip_lo_cols(data, lo_vals):
    for col in lo_vals.index.values:
        data.loc[data[col] < lo_vals[col],col] = lo_vals[col]

def rescore_metrics(data_set_path):

    current_data = reload_churn_data(data_set_path,'current','8.3',is_customer_data=True)
    load_mat_df = reload_churn_data(data_set_path,'load_mat','6.4',is_customer_data=False)
    score_df = reload_churn_data(data_set_path,'score_params','7.5',is_customer_data=False)
    stats = reload_churn_data(data_set_path,'summarystats','5.2',is_customer_data=False)
    stats.drop('is_churn',inplace=True)
    assert set(score_df.index.values)==set(current_data.columns.values),"Data to re-score does not match transform params"
    assert set(load_mat_df.index.values)==set(current_data.columns.values),"Data to re-score does not match load matrix"
    assert set(stats.index.values)==set(current_data.columns.values),"Data to re-score does not match summary stats"

    clip_hi_cols(current_data, stats['99pct'])
    clip_lo_cols(current_data, stats['1pct'])

    transform_skew_columns(current_data, score_df[score_df['skew_score']].index.values)
    transform_fattail_columns(current_data, score_df[score_df['skew_score']].index.values)

    current_data=current_data[score_df.index.values]
    scaled_data=(current_data-score_df['mean'])/score_df['std']

    scaled_data = scaled_data[load_mat_df.index.values]
    grouped_ndarray = np.matmul(scaled_data.to_numpy(), load_mat_df.to_numpy())

    current_data_grouped = pd.DataFrame(grouped_ndarray,columns=load_mat_df.columns.values, index=current_data.index)

    score_save_path=data_set_path.replace('.csv','_current_groupscore.csv')
    current_data_grouped.to_csv(score_save_path,header=True)
    print('Saving results to %s' % score_save_path)


