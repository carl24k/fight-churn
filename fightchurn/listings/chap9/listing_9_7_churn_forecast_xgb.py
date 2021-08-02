import pandas as pd
import os
import pickle
from fightchurn.listings.chap8.listing_8_4_rescore_metrics import reload_churn_data
from fightchurn.listings.chap8.listing_8_5_churn_forecast import forecast_histogram

def churn_forecast_xgb(data_set_path):

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 9.6 to save an XGB regression model first'
    with open(pickle_path, 'rb') as fid:
        xgb_model = pickle.load(fid)

    current_score_df = reload_churn_data(data_set_path,'current','8.3',is_customer_data=True)

    predictions = xgb_model.predict_proba(current_score_df.values)

    predict_df = pd.DataFrame(predictions, index=current_score_df.index, columns=['retain_prob','churn_prob'])
    forecast_save_path = data_set_path.replace('.csv', '_current_xgb_predictions.csv')
    print('Saving results to %s' % forecast_save_path)
    predict_df.to_csv(forecast_save_path, header=True)

    forecast_histogram(data_set_path,predict_df,ext='xgb')
