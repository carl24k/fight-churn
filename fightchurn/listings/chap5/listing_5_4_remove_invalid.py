import pandas as pd
import os

def remove_invalid(data_set_path,min_valid=None,max_valid=None):

    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    clean_data = churn_data.copy()

    if min_valid and isinstance(min_valid,dict):
        for metric in min_valid.keys():
            if metric in clean_data.columns.values:
                clean_data=clean_data[clean_data[metric] > min_valid[metric]]
            else:
                print('metric %s is not in the data set %s' % (metric,data_set_path))

    if max_valid and isinstance(max_valid,dict):
        for metric in max_valid.keys():
            if metric in clean_data.columns.values:
                clean_data=clean_data[clean_data[metric] < max_valid[metric]]
            else:
                print('metric %s is not in the data set %s' % (metric,data_set_path))

    score_save_path=data_set_path.replace('.csv','_cleaned.csv')
    print('Saving results to %s' % score_save_path)
    clean_data.to_csv(score_save_path,header=True)
