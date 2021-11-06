from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

from listings.chap6.listing_6_6_metric_group_transformer import HeirarchicalClusterDimReducer
from listings.chap7.listing_7_10_extreme_score_transformer import ExtremeScorer
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import make_scorer
from sklearn.linear_model import LogisticRegression

def crossvalidate_transformers(data_set_path, n_test_split):

    data_df = pd.read_csv(data_set_path,index_col=[0,1])
    y = data_df['is_churn'].astype(int)
    y=np.subtract(1,y)
    X = data_df.drop(['is_churn'],axis=1)

    scorer = ExtremeScorer(out_col=None)
    reducer = HeirarchicalClusterDimReducer(out_col=None)
    logistic = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)
    steps = [
        ('scorer', scorer),
        ('reducer', reducer),
        ('logistic', logistic)
    ]
    param_grid = {
        'scorer__skew_thresh' : [2,4,8],
        'scorer__kurt_thresh' : [4,7,15],
        'reducer__corr_thresh' : [.5, .65, .8],
        'logistic__C' : [0.32, 0.16, 0.08]
    }

    pipe = Pipeline(steps)
    tscv = TimeSeriesSplit(n_splits=n_test_split)
    score_models = {'AUC': 'roc_auc'}

    gsearch = GridSearchCV(pipe,scoring=score_models, cv=tscv, verbose=1,
                           return_train_score=False,  param_grid=param_grid, refit='AUC')

    gsearch.fit(X, y)

    result_df = pd.DataFrame(gsearch.cv_results_)
    result_df.to_csv(data_set_path.replace('.csv', '_pipeline_crossval.csv'), index=False)