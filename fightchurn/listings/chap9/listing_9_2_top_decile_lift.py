from fightchurn.listings.chap8.listing_8_2_logistic_regression import prepare_data
from fightchurn.listings.chap9.listing_9_1_regression_auc  import reload_regression
import numpy

def calc_lift(y_true, y_pred):
    if numpy.unique(y_pred).size < 10:
        return 1.0
    sort_by_pred=[(p,t) for p,t in sorted(zip(y_pred, y_true))]
    overall_churn = sum(y_true)/len(y_true)
    i90=int(round(len(y_true)*0.9))
    top_decile_count=sum([p[1] for p in sort_by_pred[i90:]])
    top_decile_churn = top_decile_count/(len(y_true)-i90)
    lift = top_decile_churn/overall_churn
    return lift

def top_decile_lift(data_set_path):

    logreg_model = reload_regression(data_set_path)
    X,y = prepare_data(data_set_path,as_retention=False)
    predictions = logreg_model.predict_proba(X)
    lift = calc_lift(y,predictions[:,0])
    print('Regression Lift score={:.3f}'.format(lift))
