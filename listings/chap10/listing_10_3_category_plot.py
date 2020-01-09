import pandas as pd
import matplotlib.pyplot as plt
import os
import statsmodels.stats.proportion as sp

def category_plot(data_set_path, category=''):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    churn_data[category].fillna('-na-',inplace=True)

    summary = churn_data.groupby(category).agg({category:'count','is_churn': ['sum','mean']})
    intervals = sp.proportion_confint(summary['is_churn','sum'],summary[ (category,'count')],method='wilson')

    summary['lo_bound'] = intervals[0]
    summary['hi_bound'] = intervals[1]
    summary['lo_bar'] = summary[('is_churn','mean')]-summary['lo_bound']
    summary['hi_bar'] = summary['hi_bound'] - summary[('is_churn','mean')]

    save_path = data_set_path.replace('.csv', '_' + category + '_churn_category.csv')
    summary.to_csv(save_path)

    n_category = summary.shape[0]
    plt.figure(figsize=(max(4,.5*n_category), 4))
    plt.bar(x=summary.index,height=summary[('is_churn','mean')],
            yerr=summary[['lo_bar','hi_bar']].transpose().values,capsize=80/n_category)
    plt.xlabel('Category Average of Churn for  "%s"' % category)
    plt.ylabel('Category Churn Rate')
    plt.grid()
    save_path = data_set_path.replace('.csv', '_' + category + '_churn_category.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)
