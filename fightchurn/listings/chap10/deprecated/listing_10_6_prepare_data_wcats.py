from fightchurn.listings.chap5.listing_5_2_dataset_stats import dataset_stats
from fightchurn.listings.chap7.listing_7_5_fat_tail_scores import fat_tail_scores
from fightchurn.listings.chap6.listing_6_3_apply_metric_groups import apply_metric_groups
from fightchurn.listings.chap6.listing_6_5_ordered_correlation_matrix import ordered_correlation_matrix
from fightchurn.listings.chap10.listing_10_5_find_groups_skip_cats import find_groups_skip_cats
from fightchurn.listings.chap10.listing_10_4_dummy_variables import dummy_variables

def prepare_data_wcats(data_set_path,groups,group_corr_thresh):
    dummy_variables(data_set_path,groups)
    dummy_data_path=data_set_path.replace('.csv', '_dumcat.csv')
    dataset_stats(dummy_data_path)
    fat_tail_scores(dummy_data_path)
    find_groups_skip_cats(dummy_data_path,group_corr_thresh)
    apply_metric_groups(dummy_data_path)
    ordered_correlation_matrix(dummy_data_path)
