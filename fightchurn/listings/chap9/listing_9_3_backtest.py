import pandas as pd
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
from sklearn.linear_model import LogisticRegression

from fightchurn.listings.chap8.listing_8_2_logistic_regression import prepare_data
from fightchurn.listings.chap9.listing_9_2_top_decile_lift import calc_lift


def backtest(data_set_path,n_test_split):

    X,y = prepare_data(data_set_path,as_retention=False)

    tscv = TimeSeriesSplit(n_splits=n_test_split)

    lift_scorer = make_scorer(calc_lift, needs_proba=True)
    score_models = {'lift': lift_scorer, 'AUC': 'roc_auc'}

    retain_reg = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)

    gsearch = GridSearchCV(estimator=retain_reg,scoring=score_models, cv=tscv, verbose=1,
                           return_train_score=False,  param_grid={'C' : [1]}, refit='AUC')

    gsearch.fit(X,y)
    result_df = pd.DataFrame(gsearch.cv_results_)

    save_path = data_set_path.replace('.csv', '_backtest.csv')
    result_df.to_csv(save_path, index=False)
    print('Saved test scores to ' + save_path)
