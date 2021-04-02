import os
import pickle
from sklearn.metrics import roc_auc_score
from listing_8_2_logistic_regression import prepare_data

def xgb_auc(data_set_path):

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 9.6 to save an XGB regression model first'
    with open(pickle_path, 'rb') as fid:
        xgb_model = pickle.load(fid)

    X,y = prepare_data(data_set_path,ext='',as_retention=False)
    predictions = xgb_model.predict_proba(X)
    auc_score = roc_auc_score(y,predictions[:,1])
    print('XGB AUC score={:.3f}'.format(auc_score))
