import pandas as pd
import numpy as np
import os

def apply_metric_groups(data_set_path):

    score_save_path=data_set_path.replace('.csv','_scores.csv')
    assert os.path.isfile(score_save_path),'You must run listing 5.3 or 7.5 to save metric scores first'
    score_data = pd.read_csv(score_save_path,index_col=[0,1])
    data_2group = score_data.drop('is_churn',axis=1)

    load_mat_path = data_set_path.replace('.csv', '_load_mat.csv')
    assert os.path.isfile(load_mat_path),'You must run listing 6.4 to save a loading matrix first'
    load_mat_df = pd.read_csv(load_mat_path, index_col=0)
    load_mat_ndarray = load_mat_df.to_numpy()

    # Make sure the data is in the same column order as the rows of the loading matrix
    ndarray_2group = data_2group[load_mat_df.index.values].to_numpy()
    grouped_ndarray = np.matmul(ndarray_2group, load_mat_ndarray)

    churn_data_grouped = pd.DataFrame(grouped_ndarray,columns=load_mat_df.columns.values, index=score_data.index)

    churn_data_grouped['is_churn'] = score_data['is_churn']

    save_path = data_set_path.replace('.csv', '_groupscore.csv')
    churn_data_grouped.to_csv(save_path,header=True)
    print('Saved grouped data  to ' + save_path)

