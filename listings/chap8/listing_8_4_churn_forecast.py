import pandas as pd
import numpy as np
import os
from listing_8_3_rescore_metrics import rescore_metrics
import pickle


def churn_forecast(data_set_path='',save=True):

    pickle_path = data_set_path.replace('.csv', '_logreg_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 8.1 to save a logistic regression model first'
    with open(pickle_path, 'rb') as fid:
        logreg_model = pickle.load(fid)

    scored_current_data = rescore_metrics(data_set_path)

    result = logreg_model.predict_proba(scored_current_data)

    if save:
        current_data_path = data_set_path.replace('dataset.csv', 'current_dataset.csv')
        current_data = pd.read_csv(current_data_path)
        current_data.set_index(['account_id', 'observation_date'], inplace=True)

        current_data['churn_prob'] = result[:, 0]
        current_data['retain_prob'] = result[:, 1]

        forecast_save_path = current_data_path.replace('.csv', '_forecasts.csv')
        print('Saving results to %s' % forecast_save_path)
        current_data.to_csv(forecast_save_path, header=True)

    return result