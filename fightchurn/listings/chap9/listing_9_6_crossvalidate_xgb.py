import pandas as pd
import pickle
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
import xgboost as xgb

from fightchurn.listings.chap8.listing_8_2_logistic_regression import prepare_data
from fightchurn.listings.chap9.listing_9_2_top_decile_lift import calc_lift
from fightchurn.listings.chap8.listing_8_5_churn_forecast import forecast_histogram

def crossvalidate_xgb(data_set_path,n_test_split):

    X,y = prepare_data(data_set_path,ext='',as_retention=False)

    tscv = TimeSeriesSplit(n_splits=n_test_split)

    score_models = {'lift': make_scorer(calc_lift, needs_proba=True), 'AUC': 'roc_auc', 'loss' : 'neg_log_loss'}

    xgb_model = xgb.XGBClassifier(objective='binary:logistic',use_label_encoder=False, eval_metric='logloss')
    test_params = { 'max_depth': [1,2,4,6],
                    'learning_rate': [0.1,0.2,0.3,0.4],
                    'n_estimators': [20,40,80,120],
                    'min_child_weight' : [3,6,9,12]}
    gsearch = GridSearchCV(estimator=xgb_model,n_jobs=-1, scoring=score_models, cv=tscv, verbose=1,
                           return_train_score=False,  param_grid=test_params,refit='loss')
    gsearch.fit(X,y,verbose=1)

    result_df = pd.DataFrame(gsearch.cv_results_)
    result_df.sort_values('mean_test_AUC',ascending=False,inplace=True)
    save_path = data_set_path.replace('.csv', '_crossval_xgb.csv')
    result_df.to_csv(save_path, index=False)
    print('Saved test scores to ' + save_path)

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    with open(pickle_path, 'wb') as fid:
        pickle.dump(gsearch.best_estimator_, fid)
    print('Saved model pickle to ' + pickle_path)

    predictions = gsearch.best_estimator_.predict_proba(X)
    predict_df = pd.DataFrame(predictions, index=X.index, columns=['retain_prob','churn_prob'])
    forecast_save_path = data_set_path.replace('.csv', '_xgb_predictions.csv')
    print('Saving results to %s' % forecast_save_path)
    predict_df.to_csv(forecast_save_path, header=True)

    forecast_histogram(data_set_path,predict_df,ext='xgb')
