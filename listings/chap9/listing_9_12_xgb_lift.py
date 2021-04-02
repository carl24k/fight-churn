import os
import pickle
from listing_8_2_logistic_regression import prepare_data
from listing_9_2_top_decile_lift import calc_lift

def xgb_lift(data_set_path):

    pickle_path = data_set_path.replace('.csv', '_xgb_model.pkl')
    assert os.path.isfile(pickle_path), 'You must run listing 9.6 or 9.10 to save an XGB churn model first'
    with open(pickle_path, 'rb') as fid:
        xgb_model = pickle.load(fid)

    X,y = prepare_data(data_set_path,ext='', as_retention=False)
    predictions = xgb_model.predict_proba(X)

    lift = calc_lift(y,predictions[:,1])
    print('XGB Lift score={:.3f}'.format(lift))
