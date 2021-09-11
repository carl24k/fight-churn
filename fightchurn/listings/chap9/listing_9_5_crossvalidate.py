import pandas as pd
import ntpath
import numpy as np

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

from fightchurn.listings.chap8.listing_8_2_logistic_regression import prepare_data
from fightchurn.listings.chap9.listing_9_2_top_decile_lift import calc_lift


def crossvalidate(data_set_path,n_test_split):

    X,y = prepare_data(data_set_path,as_retention=False)
    tscv = TimeSeriesSplit(n_splits=n_test_split)
    score_models = {'lift': make_scorer(calc_lift, needs_proba=True), 'AUC': 'roc_auc'}
    retain_reg = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)
    test_params = {'C' : [0.64, 0.32, 0.16, 0.08, 0.04, 0.02, 0.01, 0.005, 0.0025]}
    gsearch = GridSearchCV(estimator=retain_reg,scoring=score_models, cv=tscv, verbose=1,
                           return_train_score=False,  param_grid=test_params, refit=False)
    gsearch.fit(X,y)

    result_df = pd.DataFrame(gsearch.cv_results_)
    result_df['n_weights']= test_n_weights(X,y,test_params)
    result_df.to_csv(data_set_path.replace('.csv', '_crossval.csv'), index=False)
    plot_regression_test(data_set_path,result_df)

def test_n_weights(X,y,test_params):
    n_weights=[]
    for c in test_params['C']:
        lr = LogisticRegression(penalty='l1',C=c, solver='liblinear', fit_intercept=True)
        res=lr.fit(X,~y)
        n_weights.append(res.coef_[0].astype(bool).sum(axis=0))
    return n_weights

def plot_regression_test(data_set_path, result_df):
    result_df['plot_C']=result_df['param_C'].astype(str)
    plt.figure(figsize=(4,6))
    plt.rcParams.update({'font.size':8})
    one_subplot(result_df,1,'mean_test_AUC',ylim=(0.5,0.8),ytick=.05)
    plt.title(ntpath.basename(data_set_path).replace('_dataset.csv',' Cross Validation'))
    one_subplot(result_df,2,'mean_test_lift',ylim=(1, 6),ytick=0.5)
    one_subplot(result_df,3,'n_weights', ylim=(0, int(1 + result_df['n_weights'].max())),ytick=2)
    plt.xlabel('Regression C Param')
    plt.savefig(data_set_path.replace('.csv', '_crossval_regression.png'))
    plt.close()

def one_subplot(result_df,plot_n,var_name,ylim,ytick):
    ax = plt.subplot(3,1,plot_n)
    ax.plot('plot_C', var_name, data=result_df, marker='o', label=var_name)
    plt.ylim(ylim[0],ylim[1])
    plt.yticks(np.arange(ylim[0], ylim[1], step=ytick))
    plt.legend()
    plt.grid()
