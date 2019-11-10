from listing_5_2_dataset_stats import dataset_stats
from listing_8_6_trimmed_scores import trimmed_scores
from listing_6_4_find_metric_groups import find_metric_groups
from listing_6_3_apply_metric_groups import apply_metric_groups
from listing_6_5_ordered_correlation_matrix import ordered_correlation_matrix

def prepare_data(data_set_path=''):
    dataset_stats(data_set_path)
    trimmed_scores(data_set_path)
    find_metric_groups(data_set_path)
    apply_metric_groups(data_set_path)
    ordered_correlation_matrix(data_set_path)
