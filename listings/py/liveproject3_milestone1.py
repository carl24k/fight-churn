from listing_9_6_crossvalidate_xgb import crossvalidate_xgb
from listing_9_7_churn_forecast_xgb import churn_forecast_xgb
from listing_9_8_shap_explain_xgb import shap_explain_xgb

train_data_path = '/Users/carl/Documents/churn/fight-churn-output/livebook/livebook_dataset.csv'

crossvalidate_xgb(train_data_path,n_test_split=4)
shap_explain_xgb(train_data_path)
churn_forecast_xgb(train_data_path)
