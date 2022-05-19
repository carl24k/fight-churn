from fightchurn.listings.chap9.listing_9_6_crossvalidate_xgb import crossvalidate_xgb
from fightchurn.listings.chap9.listing_9_7_churn_forecast_xgb import churn_forecast_xgb
from fightchurn.listings.chap9.listing_9_8_shap_explain_xgb import shap_explain_xgb

dataset_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_dataset.csv'


crossvalidate_xgb(dataset_path, n_test_split=5, use_time=False)

churn_forecast_xgb(dataset_path)

shap_explain_xgb(dataset_path)
