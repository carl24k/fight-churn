import pandas as pd
import matplotlib.pyplot as plt
import os
import statsmodels.stats.proportion as sp


def category_plot(data_set_path, category):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    churn_data[category].fillna('-na-',inplace=True)
    summary = category_churn_summary(churn_data,category,data_set_path)
    category_churn_plot(category, summary, data_set_path)


def category_churn_summary(churn_data, category,data_set_path):
    summary = churn_data.groupby(category).agg({category:'count','is_churn': ['sum','mean']})
    intervals = sp.proportion_confint(summary['is_churn','sum'],summary[ (category,'count')],method='wilson')
    summary[category + '_percent'] = (1.0/churn_data.shape[0]) * summary[(category,'count')]
    summary['lo_conf'] = intervals[0]
    summary['hi_conf'] = intervals[1]
    summary['lo_int'] = summary[('is_churn','mean')]-summary['lo_conf']
    summary['hi_int'] = summary['hi_conf'] - summary[('is_churn','mean')]
    save_path = data_set_path.replace('.csv', '_' + category + '_churn_category.csv')
    summary.to_csv(save_path)
    return summary


def category_churn_plot(category, summary,data_set_path):
    n_category = summary.shape[0]
    plt.figure(figsize=(max(4,.5*n_category), 4))
    plt.bar(x=summary.index,height=summary[('is_churn','mean')],
            yerr=summary[['lo_int','hi_int']].transpose().values,capsize=80/n_category)
    plt.xlabel('Category Average of Churn for  "%s"' % category)
    plt.ylabel('Category Churn Rate')
    plt.grid()
    save_path = data_set_path.replace('.csv', '_' + category + '_churn_category.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)

