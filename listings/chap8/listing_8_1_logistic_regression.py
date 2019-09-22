import pandas as pd
import numpy as np
from listing_6_3_apply_metric_groups import apply_metric_groups
from sklearn.linear_model import LogisticRegression


def logistic_regression(data_set_path='',save=True):

    grouped_data= apply_metric_groups(data_set_path,save=False)

    y = ~grouped_data['is_churn']
    X = grouped_data.drop(['is_churn'],axis=1)

    LogReg = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)
    LogReg.fit(X, y)

    full_list = ['offset']
    full_list.extend(X.columns.values)
    all_coef = [float(LogReg.intercept_)]
    all_coef.extend(list(LogReg.coef_[0]))
    results_dict = {'metric': full_list, 'coef': all_coef}
    result_df = pd.DataFrame.from_dict(results_dict)

    if save:
        save_path = data_set_path.replace('.csv', '_logreg_coef.csv')
        result_df.to_csv(save_path, index=False)
        print('Saved result to ' + save_path)
    return result_df