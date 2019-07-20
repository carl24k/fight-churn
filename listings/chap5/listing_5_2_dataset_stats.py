import pandas as pd

def dataset_stats(data_set_path='',save=True):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    churn_data['is_churn']=churn_data['is_churn'].astype(float)

    summary = churn_data.describe()
    summary = summary.transpose()

    summary['skew'] = churn_data.skew()
    summary['1%'] = churn_data.quantile(q=0.01)
    summary['99%'] = churn_data.quantile(q=0.99)
    summary['nonzero'] = churn_data.astype(bool).sum(axis=0) / churn_data.shape[0]

    summary = summary[ ['count','nonzero','mean','std','skew','min','1%','25%','50%','75%','99%','max'] ]

    if save:
        save_path = data_set_path.replace('.csv', '_summarystats.csv')
        summary.to_csv(save_path,header=True)
        print('Saving results to %s' % save_path)

    return summary
