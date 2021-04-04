from listing_5_2_dataset_stats import dataset_stats
from listing_7_5_fat_tail_scores import fat_tail_scores
from listing_9_5_crossvalidate import  crossvalidate
from listing_9_4_regression_cparam import regression_cparam
from listing_6_4_find_metric_groups import find_metric_groups
from listing_6_3_apply_metric_groups import apply_metric_groups
from listing_6_5_ordered_correlation_matrix import ordered_correlation_matrix
from listing_8_5_churn_forecast import churn_forecast
from listing_8_6_rescore_metrics import rescore_metrics

train_data_path = '/Users/carl/Documents/churn/fight-churn-output/livebook/livebook_dataset.csv'

def prepare_data():
    dataset_stats(train_data_path)
    fat_tail_scores(train_data_path)
    find_metric_groups(train_data_path,group_corr_thresh=0.75)
    apply_metric_groups(train_data_path)
    ordered_correlation_matrix(train_data_path)

def train():
    crossvalidate(train_data_path,n_test_split=2)

def score():
    regression_cparam(train_data_path,0.04)
    rescore_metrics(train_data_path)
    churn_forecast(train_data_path,model_name='logreg_model_c0.040')

if __name__=='__main__':
    prepare_data()
    train()
    score()
