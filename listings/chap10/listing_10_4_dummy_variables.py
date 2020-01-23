import pandas as pd
from copy import copy

from listing_10_3_grouped_category_cohorts import group_category_column

def dummy_variables(data_set_path, groups={},current=False):

    raw_data = pd.read_csv(data_set_path, index_col=[0, 1])

    for cat in groups.keys():
        group_category_column(raw_data,cat,groups[cat])

    data_w_dummies = pd.get_dummies(raw_data)
    if not current:
        save_path = data_set_path.replace('.csv', '_dumcat.csv')
    else:
        save_path = data_set_path.replace('current.csv', 'dumcat_current.csv')

    data_w_dummies.to_csv(save_path,header=True)
    print('Saved data with dummies  to ' + save_path)

    new_cols = sorted(list(set(data_w_dummies.columns).difference(set(raw_data.columns))))
    pd.DataFrame(new_cols).to_csv(data_set_path.replace('.csv', '_dummylist.csv'),header=False,index=False)
    new_cols.append('is_churn')
    save_path = data_set_path.replace('.csv', '_onlydummies.csv')
    print('Saved dummy variable only dataset ' + save_path)
    data_w_dummies[new_cols].to_csv(save_path)

    return new_cols
