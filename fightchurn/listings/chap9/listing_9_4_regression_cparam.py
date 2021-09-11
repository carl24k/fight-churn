from sklearn.linear_model import LogisticRegression
from fightchurn.listings.chap8.listing_8_2_logistic_regression import prepare_data, save_regression_model
from fightchurn.listings.chap8.listing_8_2_logistic_regression import save_regression_summary, save_dataset_predictions

def regression_cparam(data_set_path, C_param):
    X,y = prepare_data(data_set_path)
    retain_reg = LogisticRegression( C=C_param, penalty='l1', solver='liblinear', fit_intercept=True)
    retain_reg.fit(X, y)
    c_ext = '_c{:.3f}'.format(C_param)
    save_regression_summary(data_set_path,retain_reg,ext=c_ext)
    save_regression_model(data_set_path,retain_reg,ext=c_ext)
    save_dataset_predictions(data_set_path,retain_reg,X,ext=c_ext)

