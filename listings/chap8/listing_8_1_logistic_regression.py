import pandas as pd
import numpy as np
from listing_6_3_apply_metric_groups import apply_metric_groups
from sklearn.linear_model import LogisticRegression
import pickle

def coefs_to_dataframe(log_reg, column_names):
    full_list = ['offset']
    full_list.extend(column_names)
    all_coef = [float(log_reg.intercept_)]
    all_coef.extend(list(log_reg.coef_[0]))
    results_dict = {'metric': full_list, 'coef': all_coef}
    result_df = pd.DataFrame.from_dict(results_dict)
    return result_df

def logistic_regression(data_set_path='',save=True):

    grouped_data= apply_metric_groups(data_set_path,save=False)

    y = ~grouped_data['is_churn']
    X = grouped_data.drop(['is_churn'],axis=1)

    retain_reg = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)
    retain_reg.fit(X, y)

    if save:
        coef_df = coefs_to_dataframe(retain_reg, X.columns.values)
        save_path = data_set_path.replace('.csv', '_logreg_coef.csv')
        coef_df.to_csv(save_path, index=False)
        print('Saved coefficients to ' + save_path)

        pickle_path = data_set_path.replace('.csv', '_logreg_model.pkl')
        with open(pickle_path, 'wb') as fid:
            pickle.dump(retain_reg, fid)
        print('Saved model pickle to ' + pickle_path)

    return retain_reg
