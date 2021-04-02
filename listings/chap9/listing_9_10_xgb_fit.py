import pandas as pd
import pickle
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
import xgboost as xgb

from listing_8_2_logistic_regression import prepare_data
from listing_8_5_churn_forecast import forecast_histogram

def xgb_fit(data_set_path):

    X,y = prepare_data(data_set_path,ext='',as_retention=False)
    xgb_model = xgb.XGBClassifier(objective='binary:logistic',use_label_encoder=False, eval_metric='logloss')
                                  # max_depth=1,n_estimators=120,min_child_weight=12,learning_rate=0.2) # best params
    xgb_model.fit(X,y)

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    with open(pickle_path, 'wb') as fid:
        pickle.dump(xgb_model, fid)
    print('Saved model pickle to ' + pickle_path)

    predictions = xgb_model.predict_proba(X.values)
    predict_df = pd.DataFrame(predictions, index=X.index, columns=['retain_prob','churn_prob'])
    forecast_save_path = data_set_path.replace('.csv', '_xgb_predictions.csv')
    print('Saving results to %s' % forecast_save_path)
    predict_df.to_csv(forecast_save_path, header=True)

    forecast_histogram(data_set_path,predict_df,ext='xgb')
