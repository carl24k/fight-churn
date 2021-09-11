from fightchurn.listings.chap5.listing_5_2_dataset_stats import dataset_stats
from fightchurn.listings.chap7.listing_7_5_fat_tail_scores import fat_tail_scores
from fightchurn.listings.chap6.listing_6_4_find_metric_groups import find_metric_groups
from fightchurn.listings.chap6.listing_6_3_apply_metric_groups import apply_metric_groups
from fightchurn.listings.chap6.listing_6_5_ordered_correlation_matrix import ordered_correlation_matrix

def prepare_data(data_set_path,group_corr_thresh=0.55):
    dataset_stats(data_set_path)
    fat_tail_scores(data_set_path)
    find_metric_groups(data_set_path,group_corr_thresh)
    apply_metric_groups(data_set_path)
    ordered_correlation_matrix(data_set_path)
