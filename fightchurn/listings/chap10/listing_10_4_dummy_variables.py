import pandas as pd

from fightchurn.listings.chap10.listing_10_3_grouped_category_cohorts import group_category_column

def dummy_variables(data_set_path, groups={},current=False):

    raw_data = pd.read_csv(data_set_path, index_col=[0, 1])

    for cat in groups.keys():
        group_category_column(raw_data,cat,groups[cat])

    data_w_dummies = pd.get_dummies(raw_data,dummy_na=True)
    new_cols = sorted(list(set(data_w_dummies.columns).difference(set(raw_data.columns))))
    cat_cols = sorted(list(set(raw_data.columns).difference(set(data_w_dummies.columns))))
    dummy_col_df = pd.DataFrame(new_cols,index=new_cols,columns=['metrics'])
    dummy_col_df.to_csv(data_set_path.replace('.csv', '_dummies_groupmets.csv'))

    if not current:
        new_cols.append('is_churn')
        data_w_dummies.to_csv(data_set_path.replace('.csv', '_xgbdummies.csv'))
    else:
        data_w_dummies.to_csv(data_set_path.replace('current.csv', 'xgbdummies_current.csv'))

    dummies_only = data_w_dummies[new_cols]
    save_path = data_set_path.replace('.csv', '_dummies_groupscore.csv')
    print('Saved dummy variable (only) dataset ' + save_path)
    dummies_only.to_csv(save_path)

    raw_data.drop(cat_cols,axis=1,inplace=True)
    save_path = data_set_path.replace('.csv', '_nocat.csv')
    print('Saved no category dataset ' + save_path)
    raw_data.to_csv(save_path)
