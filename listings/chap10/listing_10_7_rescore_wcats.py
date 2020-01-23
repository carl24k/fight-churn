
from listing_7_5_fat_tail_scores import transform_fattail_columns, transform_skew_columns
from listing_8_4_rescore_metrics import score_current_data, group_current_data, reload_churn_data
from listing_10_4_dummy_variables import dummy_variables

def rescore_wcats(data_set_path,categories,groups):

    dummy_path = data_set_path.replace('.csv', '_dumcat.csv')
    load_mat_df = reload_churn_data(dummy_path,'load_mat','6.4',is_customer_data=False)
    score_df = reload_churn_data(dummy_path,'score_params','7.5',is_customer_data=False)

    current_path = data_set_path.replace('.csv', '_current.csv')
    new_dummies = set(dummy_variables(current_path,groups, current=True))

    current_data = reload_churn_data(data_set_path,'dumcat_current','10.7',is_customer_data=True)
    assert set(score_df.index.values)==set(current_data.columns.values),"Data to re-score does not match transform params"
    assert set(load_mat_df.index.values)==set(current_data.columns.values),"Data to re-score does not match loading matrix"

    align_dummies(current_data,data_set_path,new_dummies)

    transform_skew_columns(current_data,score_df[score_df['skew_score']].index.values)
    transform_fattail_columns(current_data,score_df[score_df['fattail_score']].index.values)
    scaled_data = score_current_data(current_data,score_df,data_set_path)
    grouped_data = group_current_data(scaled_data, load_mat_df,data_set_path)

    current_data_orig = reload_churn_data(data_set_path,'current','10.7',is_customer_data=True)
    save_segment_data_wcats(grouped_data,current_data_orig,load_mat_df,data_set_path, categories)


def align_dummies(current_data,data_set_path,new_dummies):
    with open(data_set_path.replace('.csv', '_onlydummies_groupmets.csv')) as f:
        assert False, "fix this"
        old_dummies = set(f.read().splitlines() )
    missing_in_old = new_dummies.difference(old_dummies)
    missing_in_new = old_dummies.difference(new_dummies)
    for col in missing_in_new:
        current_data[col]=0.0
    for col in missing_in_old:
        current_data.drop(col,axis=1,inplace=True)


def save_segment_data_wcats(current_data_grouped, current_data, load_mat_df, data_set_path, categories):

    group_cols =  load_mat_df.columns[load_mat_df.astype(bool).sum(axis=0) > 1]
    no_group_cols = load_mat_df.columns[load_mat_df.astype(bool).sum(axis=0) == 1]
    no_group_cols = [col for col in no_group_cols if not any([col.startswith(cat) for cat in categories])]
    no_group_cols.extend(categories)
    segment_df = current_data_grouped[group_cols].join(current_data[no_group_cols])
    segment_df.to_csv(data_set_path.replace('.csv','_current_groupmets_segment.csv'),header=True)