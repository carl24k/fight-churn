import pandas as pd
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
import xgboost as xgb
from listing_8_2_logistic_regression import prepare_data
from listing_9_2_top_decile_lift import calc_lift


def backtest_xgb(data_set_path,n_test_split):

    X,y = prepare_data(data_set_path,as_retention=False)

    tscv = TimeSeriesSplit(n_splits=n_test_split)

    lift_scorer = make_scorer(calc_lift, needs_proba=True)
    score_models = {'lift': lift_scorer, 'AUC': 'roc_auc', 'loss' : 'neg_log_loss'}

    xgb_model = xgb.XGBClassifier(objective='binary:logistic',use_label_encoder=False, eval_metric='logloss')
    the_params = { 'max_depth': [1],'learning_rate': [0.2],'n_estimators': [120],'min_child_weight' : [12]}
    gsearch = GridSearchCV(estimator=xgb_model,n_jobs=-1, scoring=score_models, cv=tscv, verbose=1,
                           return_train_score=False,  param_grid=the_params,refit='loss')
    gsearch.fit(X,y,verbose=1)

    gsearch.fit(X,y)
    result_df = pd.DataFrame(gsearch.cv_results_)

    save_path = data_set_path.replace('.csv', '_backtest_xgb.csv')
    result_df.to_csv(save_path, index=False)
    print('Saved test scores to ' + save_path)
