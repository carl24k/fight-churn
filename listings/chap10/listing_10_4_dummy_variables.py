import pandas as pd

from listing_10_3_grouped_category_plot import group_category_column

def dummy_variables(data_set_path,columns, groups={}):

    raw_data = pd.read_csv(data_set_path, index_col=[0, 1])

    for cat in groups.keys():
        group_cat_col = group_category_column(raw_data,cat,groups[cat])
        columns.remove(cat)
        columns.append(group_cat_col)

    new_data = raw_data.drop(columns,axis=1)

    for c in columns:
        dummies = raw_data[c].str.get_dummies()
        dummies.columns=['{}_{}'.format(c,str(cat)) for cat in dummies.columns]
        new_data = new_data.join(dummies)


    save_path = data_set_path.replace('.csv', '_dumcat.csv')
    new_data.to_csv(save_path,header=True)
    print('Saved data with dummies  to ' + save_path)
