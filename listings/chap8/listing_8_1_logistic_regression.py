import pandas as pd
import numpy as np
from listing_6_3_apply_metric_groups import apply_metric_groups
from sklearn.linear_model import LogisticRegression
import pickle


def logistic_regression(data_set_path='',save=True):

    grouped_data= apply_metric_groups(data_set_path,save=False)

    y = ~grouped_data['is_churn']
    X = grouped_data.drop(['is_churn'],axis=1)

    retain_reg = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)
    retain_reg.fit(X, y)

    if save:
        coef_df = pd.DataFrame.from_dict(
            {'metric':  np.append(X.columns.values,'offset'),
             'coef': np.append(retain_reg.coef_[0],retain_reg.intercept_)})
        save_path = data_set_path.replace('.csv', '_logreg_coef.csv')
        coef_df.to_csv(save_path, index=False)
        print('Saved coefficients to ' + save_path)

        pickle_path = data_set_path.replace('.csv', '_logreg_model.pkl')
        with open(pickle_path, 'wb') as fid:
            pickle.dump(retain_reg, fid)
        print('Saved model pickle to ' + pickle_path)

    return retain_reg
