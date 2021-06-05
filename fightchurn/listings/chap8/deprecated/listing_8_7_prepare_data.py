from listing_5_2_dataset_stats import dataset_stats
from listing_8_6_clipped_scores import clipped_scores
from listing_6_4_find_metric_groups import find_metric_groups
from listing_6_3_apply_metric_groups import apply_metric_groups

def prepare_data(data_set_path):
    dataset_stats(data_set_path)
    clipped_scores(data_set_path)
    find_metric_groups(data_set_path)
    apply_metric_groups(data_set_path)
