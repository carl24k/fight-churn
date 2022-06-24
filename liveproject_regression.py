from fightchurn.listings.chap8.listing_8_1_prepare_data import prepare_data
from fightchurn.listings.chap9.listing_9_5_crossvalidate import crossvalidate
from fightchurn.listings.chap9.listing_9_4_regression_cparam import regression_cparam
from fightchurn.listings.chap8.listing_8_4_rescore_metrics import rescore_metrics
from fightchurn.listings.chap8.listing_8_5_churn_forecast import churn_forecast

dataset_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_dataset.csv'

CORRELATION_THRESHOLD = 0.75
REGRESSION_C_PARAM = 0.02

prepare_data(dataset_path, CORRELATION_THRESHOLD)
crossvalidate(dataset_path,5)
regression_cparam(dataset_path,REGRESSION_C_PARAM)
rescore_metrics(dataset_path)
churn_forecast(dataset_path, f'logreg_model_c{REGRESSION_C_PARAM:.3f}')
