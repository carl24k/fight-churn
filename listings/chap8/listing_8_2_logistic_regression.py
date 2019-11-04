import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
import pickle


def logistic_regression(data_set_path='',save=True):

    score_save_path = data_set_path.replace('.csv', '_groupscore.csv')
    assert os.path.isfile(score_save_path), 'You must run listing 6.3 to save grouped metric scores first'
    grouped_data = pd.read_csv(score_save_path)
    grouped_data.set_index(['account_id', 'observation_date'], inplace=True)
    group_lists = pd.read_csv(data_set_path.replace('.csv', '_groupmets.csv'))

    y = ~grouped_data['is_churn']
    X = grouped_data.drop(['is_churn'],axis=1)

    retain_reg = LogisticRegression(penalty='l1', solver='liblinear', fit_intercept=True)
    retain_reg.fit(X, y)

    if save:
        coef_df = pd.DataFrame.from_dict(
            {'group':  np.append(X.columns.values,'offset'),
             'coef': np.append(retain_reg.coef_[0],retain_reg.intercept_),
             'metrics' : np.append(group_lists['metrics'],'NA')})
        save_path = data_set_path.replace('.csv', '_logreg_coef.csv')
        coef_df.to_csv(save_path, index=False)
        print('Saved coefficients to ' + save_path)

        pickle_path = data_set_path.replace('.csv', '_logreg_model.pkl')
        with open(pickle_path, 'wb') as fid:
            pickle.dump(retain_reg, fid)
        print('Saved model pickle to ' + pickle_path)

        predictions = retain_reg.predict_proba(X)
        predict_df = pd.DataFrame(predictions,index=grouped_data.index,columns=['churn_prob','retain_prob'])
        predict_path = data_set_path.replace('.csv', '_predictions.csv')
        predict_df.to_csv(predict_path,header=True)
        print('Saved predictions to ' + predict_path)

    return retain_reg
