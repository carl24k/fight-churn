import pandas as pd
import os

def dataset_stats(data_set_path):

    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    if 'is_churn' in churn_data:
        churn_data['is_churn']=churn_data['is_churn'].astype(float)

    summary = churn_data.describe()
    summary = summary.transpose()

    summary['skew'] = churn_data.skew()
    summary['1%'] = churn_data.quantile(q=0.01)
    summary['99%'] = churn_data.quantile(q=0.99)
    summary['nonzero'] = churn_data.astype(bool).sum(axis=0) / churn_data.shape[0]

    summary = summary[ ['count','nonzero','mean','std','skew','min','1%','25%','50%','75%','99%','max'] ]
    summary.columns = summary.columns.str.replace("%", "pct")

    save_path = data_set_path.replace('.csv', '_summarystats.csv')
    summary.to_csv(save_path,header=True)
    print('Saving results to %s' % save_path)

