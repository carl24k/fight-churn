import pandas as pd
import matplotlib.pyplot as plt
import os
import statsmodels.stats.proportion as sp

def grouped_category_plot(data_set_path, category, groups):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    churn_data[category].fillna('-na-',inplace=True)

    group_lookup = {value: key for key in groups.keys() for value in groups[key]}
    group_cat_col = category + '_group'
    churn_data[group_cat_col] = churn_data[category].apply(lambda x: group_lookup[x] if x in group_lookup else x)

    summary = churn_data.groupby(group_cat_col).agg({group_cat_col:'count','is_churn': ['sum','mean']})
    intervals = sp.proportion_confint(summary['is_churn','sum'],summary[ (group_cat_col,'count')],method='wilson')
    summary[group_cat_col + '_percent'] = (1.0/churn_data.shape[0]) * summary[(group_cat_col,'count')]
    summary['lo_bound'] = intervals[0]
    summary['hi_bound'] = intervals[1]
    summary['lo_bar'] = summary[('is_churn','mean')]-summary['lo_bound']
    summary['hi_bar'] = summary['hi_bound'] - summary[('is_churn','mean')]

    save_path = data_set_path.replace('.csv', '_' + group_cat_col + '_churn_category.csv')
    print('Saving data to %s' % save_path)
    summary.to_csv(save_path)

    n_category = summary.shape[0]
    plt.figure(figsize=(max(4,.5*n_category), 4))
    plt.bar(x=summary.index,height=summary[('is_churn','mean')],
            yerr=summary[['lo_bar','hi_bar']].transpose().values,capsize=80/n_category)
    plt.xlabel('Category Average of Churn for  "%s"' % group_cat_col)
    plt.ylabel('Category Churn Rate')
    plt.grid()
    save_path = data_set_path.replace('.csv', '_' + group_cat_col + '_churn_category.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)
