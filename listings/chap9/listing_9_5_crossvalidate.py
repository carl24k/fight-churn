import pandas as pd
import ntpath
import numpy as np
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

from listing_8_2_logistic_regression import prepare_data
from listing_9_1_regression_auc import reload_regression
from listing_9_2_top_decile_lift import calc_lift


def crossvalidate(data_set_path):

    X,y = prepare_data(data_set_path)
    y=~y

    tscv = TimeSeriesSplit(n_splits=3)

    lift_scorer = make_scorer(calc_lift, needs_proba=True)
    score_models = {'lift_scorer': lift_scorer, 'AUC': 'roc_auc'}

    retain_reg = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)
    test_params = {'C' : [1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.015, 0.01 ]}

    gsearch = GridSearchCV(estimator=retain_reg,scoring=score_models, cv=tscv, verbose=4,
                           return_train_score=False,  param_grid=test_params, refit='AUC')

    n_weights=[]
    for c in test_params['C']:
        lr = LogisticRegression(penalty='l1',C=c, solver='liblinear', fit_intercept=True)
        res=lr.fit(X,~y)
        n_weights.append(res.coef_[0].astype(bool).sum(axis=0))

    gsearch.fit(X,y)
    result_df = pd.DataFrame(gsearch.cv_results_)
    result_df['n_weights']=n_weights

    save_path = data_set_path.replace('.csv', '_crossval.csv')
    result_df.to_csv(save_path, index=False)
    print('Saved test scores to ' + save_path)

    def pretty_plot(ylim1,ylim2,ytick):
        plt.ylim(ylim1,ylim2)
        plt.yticks(np.arange(ylim1, ylim2, step=ytick))
        plt.legend()
        plt.grid()

    result_df['plot_C']=result_df['param_C'].astype(str)
    plt.figure(figsize=(8, 10))

    plt.subplot(3, 1, 1)
    plt.plot('plot_C', 'mean_test_AUC', data=result_df, marker='o', color='black', linewidth=2, label="AUC")
    pretty_plot(0.6,0.8,0.05)
    plt.title(ntpath.basename(data_set_path).replace('_dataset.csv',' Cross Validation'))

    plt.subplot(3, 1, 2)
    plt.plot('plot_C', 'mean_test_lift_scorer', data=result_df, marker='o', color='black', linewidth=2, label="AUC")
    pretty_plot(2, 4,0.5)

    plt.subplot(3, 1, 3)
    plt.plot('plot_C', 'n_weights', data=result_df, marker='o', color='black', linewidth=2, label="# Weights > 0")
    pretty_plot(0, int(1 + result_df['n_weights'].max()),2)
    plt.xlabel('Regression C Param')

    save_path = data_set_path.replace('.csv', '_crossval.png')
    plt.savefig(save_path)
    plt.close()