import pandas as pd
import os

from fightchurn.listings.chap10.listing_10_2_category_churn_cohorts import category_churn_summary, category_churn_plot, prepare_category_data



def grouped_category_cohorts(data_set_path, cat_col, groups):

    churn_data = prepare_category_data(data_set_path,cat_col)

    group_cat_col = group_category_column(churn_data,cat_col,groups)

    summary = category_churn_summary(churn_data,group_cat_col,data_set_path)

    category_churn_plot(group_cat_col, summary, data_set_path)

def group_category_column(df, cat_col, group_dict):
    group_lookup = {value: key for key in group_dict.keys() for value in group_dict[key]}
    group_cat_col = cat_col + '_group'
    df[group_cat_col] = df[cat_col].apply(lambda x: group_lookup[x] if x in group_lookup else x)
    df.drop(cat_col,axis=1,inplace=True)
    return group_cat_col