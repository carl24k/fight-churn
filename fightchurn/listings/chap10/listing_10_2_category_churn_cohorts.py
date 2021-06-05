import pandas as pd
import matplotlib.pyplot as plt
import os
import statsmodels.stats.proportion as sp


def category_churn_cohorts(data_set_path, cat_col):
    churn_data = prepare_category_data(data_set_path,cat_col)
    summary = category_churn_summary(churn_data,cat_col,data_set_path)
    category_churn_plot(cat_col, summary, data_set_path)

def prepare_category_data(data_set_path,cat_col):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    churn_data[cat_col].fillna('-na-',inplace=True)
    return churn_data

def category_churn_summary(churn_data, cat_col,data_set_path):
    summary = churn_data.groupby(cat_col).agg({cat_col:'count','is_churn': ['sum','mean']})
    intervals = sp.proportion_confint(summary['is_churn','sum'],summary[ (cat_col,'count')],method='wilson')
    summary[cat_col + '_percent'] = (1.0/churn_data.shape[0]) * summary[(cat_col,'count')]
    summary['lo_conf'] = intervals[0]
    summary['hi_conf'] = intervals[1]
    summary['lo_int'] = summary[('is_churn','mean')]-summary['lo_conf']
    summary['hi_int'] = summary['hi_conf'] - summary[('is_churn','mean')]
    save_path = data_set_path.replace('.csv', '_' + cat_col + '_churn_category.csv')
    summary.to_csv(save_path)
    return summary


def category_churn_plot(cat_col, summary,data_set_path):
    n_category = summary.shape[0]
    plt.figure(figsize=(max(4,.5*n_category), 4))
    plt.bar(x=summary.index,height=summary[('is_churn','mean')],
            yerr=summary[['lo_int','hi_int']].transpose().values,capsize=80/n_category)
    plt.xlabel('Category Average of Churn for  "%s"' % cat_col)
    plt.ylabel('Category Churn Rate')
    plt.grid()
    save_path = data_set_path.replace('.csv', '_' + cat_col + '_churn_category.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)

