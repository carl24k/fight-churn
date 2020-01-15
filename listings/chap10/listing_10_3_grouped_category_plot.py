import pandas as pd
import os

from listing_10_2_category_plot import category_churn_summary, category_churn_plot



def grouped_category_plot(data_set_path, category, groups):

    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])

    churn_data[category].fillna('-na-',inplace=True)

    group_cat_col = group_category_column(churn_data,category,groups)

    summary = category_churn_summary(churn_data,group_cat_col,data_set_path)

    category_churn_plot(group_cat_col, summary, data_set_path)

def group_category_column(df, cat_col, group_dict):
    group_lookup = {value: key for key in group_dict.keys() for value in group_dict[key]}
    group_cat_col = cat_col + '_group'
    df[group_cat_col] = df[cat_col].apply(lambda x: group_lookup[x] if x in group_lookup else x)
    df.drop(cat_col,axis=1,inplace=True)
    return group_cat_col