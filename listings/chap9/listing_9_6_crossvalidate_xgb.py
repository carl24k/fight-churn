import pandas as pd
import pickle
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
import xgboost as xgb

from listing_8_2_logistic_regression import prepare_data
from listing_9_2_top_decile_lift import calc_lift


def crossvalidate_xgb(data_set_path,n_test_split):

    X,y = prepare_data(data_set_path,ext='',as_retention=False)

    tscv = TimeSeriesSplit(n_splits=n_test_split)

    score_models = {'lift': make_scorer(calc_lift, needs_proba=True), 'AUC': 'roc_auc'}

    xgb_model = xgb.XGBClassifier(objective='binary:logistic')
    test_params = { 'max_depth': [1,2,4,6],
                    'learning_rate': [0.1,0.2,0.3,0.4],
                    'n_estimators': [20,40,80,120],
                    'min_child_weight' : [3,6,9,12]}
    gsearch = GridSearchCV(estimator=xgb_model,n_jobs=-1, scoring=score_models, cv=tscv, verbose=1,
                           return_train_score=False,  param_grid=test_params,refit=False)
    gsearch.fit(X,y)

    result_df = pd.DataFrame(gsearch.cv_results_)
    result_df.sort_values('mean_test_AUC',ascending=False,inplace=True)
    save_path = data_set_path.replace('.csv', '_crossval_xgb.csv')
    result_df.to_csv(save_path, index=False)
    print('Saved test scores to ' + save_path)

    X,y = prepare_data(data_set_path,ext='',as_retention=True)

    best_model = xgb.XGBClassifier(objective='binary:logistic',
                                   max_depth=result_df.loc[0,'param_max_depth'],learning_rate=result_df.loc[0,'param_learning_rate'],
                                   n_estimators=result_df.loc[0,'param_n_estimators'],min_child_weight=result_df.loc[0,'param_min_child_weight'])
    best_model.fit(X.values,y)

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    with open(pickle_path, 'wb') as fid:
        pickle.dump(best_model, fid)
    print('Saved model pickle to ' + pickle_path)
