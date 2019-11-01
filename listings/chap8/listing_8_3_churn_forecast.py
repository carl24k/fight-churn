import pandas as pd
import numpy as np
import os
from listing_6_3_apply_metric_groups import apply_metric_groups
from sklearn.linear_model import LogisticRegression
import pickle

def rescore_data(X, transform_df, load_mat_df):

    for col in transform_df[transform_df['skew_score']].index.values:
        X[col]=np.log(1.0+X[col])

    for col in transform_df[transform_df['fattail_score']].index.values:
        X[col]=np.log(X[col] + np.sqrt(np.power(X[col],2) + 1.0) )

    assert set(transform_df.index.values)==set(X.columns.values),"Data to re-score does not match transform params"
    X=X[transform_df.index.values]
    X=(X-transform_df['mean'])/transform_df['std']

    assert set(load_mat_df.index.values)==set(X.columns.values),"Data to re-score does not match load matrix"
    ndarray_2group = X[load_mat_df.index.values].to_numpy()
    grouped_ndarray = np.matmul(ndarray_2group, load_mat_df.to_numpy())

    return grouped_ndarray

def churn_forecast(data_set_path=''):

    load_mat_path = data_set_path.replace('.csv', '_load_mat.csv')
    assert os.path.isfile(load_mat_path),'You must run listing 6.4 to save a loading matrix first'
    load_mat_df = pd.read_csv(load_mat_path, index_col=0)

    score_param_save_path = data_set_path.replace('.csv', '_score_params.csv')
    assert os.path.isfile(score_param_save_path),'You must run listing 7.3 to save score params first'
    transform_df = pd.read_csv(score_param_save_path, index_col=0)

    pickle_path = data_set_path.replace('.csv', '_logreg_model.pkl')
    assert os.path.isfile(pickle_path),'You must run listing 8.1 to save a logistic regression model first'
    with open(pickle_path, 'rb') as fid:
        logreg_model = pickle.load(fid)

    current_data_path = data_set_path.replace('dataset.csv','current_dataset.csv')
    assert os.path.isfile(current_data_path),'You must run listing 8.2 to save a current customer data set first'
    current_data = pd.read_csv(current_data_path)
    current_data.set_index(['account_id','observation_date'],inplace=True)

    scored_current_data = rescore_data(current_data,transform_df,load_mat_df)

    result = logreg_model.predict_proba(scored_current_data)
    current_data['churn_prob'] = result[:,0]
    current_data['retain_prob'] = result[:,1]

    forecast_save_path=current_data_path.replace('.csv','_forecasts.csv')
    print('Saving results to %s' % forecast_save_path)
    current_data.to_csv(forecast_save_path,header=True)
