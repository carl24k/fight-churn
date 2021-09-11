import os
import pickle
from sklearn.metrics import roc_auc_score
from fightchurn.listings.chap8.listing_8_2_logistic_regression import prepare_data

def reload_regression(data_set_path):
    pickle_path = data_set_path.replace('.csv', '_logreg_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 8.2 to save a logistic regression model first'
    with open(pickle_path, 'rb') as fid:
        logreg_model = pickle.load(fid)
    return logreg_model

def regression_auc(data_set_path):

    logreg_model = reload_regression(data_set_path)
    X,y = prepare_data(data_set_path)
    predictions = logreg_model.predict_proba(X)
    auc_score = roc_auc_score(y,predictions[:,1])
    print('Regression AUC score={:.3f}'.format(auc_score))
