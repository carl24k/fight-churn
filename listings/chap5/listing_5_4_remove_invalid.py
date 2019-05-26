import pandas as pd

def remove_invalid(data_set_path='dataset.csv',min_valid={},max_valid={},save_path='cleaned_data.csv'):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    clean_data = churn_data.copy()

    for metric in min_valid.keys():
        if metric in clean_data.columns.values:
            clean_data=clean_data[clean_data[metric] > min_valid[metric]]
        else:
            print('metric %s is not in the data set %s' % (metric,data_set_path))

    for metric in max_valid.keys():
        if metric in clean_data.columns.values:
            clean_data=clean_data[clean_data[metric] < max_valid[metric]]
        else:
            print('metric %s is not in the data set %s' % (metric,data_set_path))

    if save_path is not None:
        clean_data.to_csv(save_path,header=True)

    return clean_data
