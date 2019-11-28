from listing_5_2_dataset_stats import dataset_stats
from listing_7_5_fat_tail_scores import fat_tail_scores
from listing_6_4_find_metric_groups import find_metric_groups
from listing_6_3_apply_metric_groups import apply_metric_groups

def prepare_data(data_set_path):
    dataset_stats(data_set_path)
    fat_tail_scores(data_set_path)
    find_metric_groups(data_set_path)
    apply_metric_groups(data_set_path)
