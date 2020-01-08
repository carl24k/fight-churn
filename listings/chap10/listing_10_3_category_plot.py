import pandas as pd
import matplotlib.pyplot as plt
import os

def category_plot(data_set_path, category=''):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])

    churn_rates = churn_data.groupby(category)['is_churn'].mean()

    plt.figure(figsize=(8, 4))
    plt.bar(x=churn_rates.index,height=churn_rates.values)
    plt.xlabel('Cohort Average of Churn for  "%s"' % category)
    plt.ylabel('Cohort Churn Rate')
    plt.grid()
    save_path = data_set_path.replace('.csv', '_' + category + '_churn_corhort.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)
