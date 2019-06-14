import pandas as pd
import numpy as np
from listing_5_2_dataset_stats import dataset_stats

def metric_scores(data_set_path='',skew_thresh=4.0,save_path='scores.csv'):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    data_scores = churn_data.copy()
    data_scores.drop('is_churn',axis=1)

    stats = dataset_stats(data_set_path)
    stats=stats.drop('is_churn')
    skewed_columns=(stats['skew']>skew_thresh) & (stats['min'] >= 0)
    skewed_columns=skewed_columns[skewed_columns]

    for col in skewed_columns.keys():
        data_scores[col]=np.log(1.0+data_scores[col])

    data_scores=(data_scores-data_scores.mean())/data_scores.std()
    data_scores['is_churn']=churn_data['is_churn']

    if save_path is not None:
        data_scores.to_csv(save_path,header=True)

    return data_scores
