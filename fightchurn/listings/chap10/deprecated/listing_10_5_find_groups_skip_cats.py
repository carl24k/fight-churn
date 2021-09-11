import os
import pandas as pd
from fightchurn.listings.chap6.listing_6_4_find_metric_groups import find_correlation_clusters, relabel_clusters, make_load_matrix, save_load_matrix

def find_groups_skip_cats(data_set_path,group_corr_thresh=0.5):

    score_save_path=data_set_path.replace('.csv','_scores.csv')
    assert os.path.isfile(score_save_path),'You must run listing 5.3 or 7.5 to save metric scores first'
    score_data = pd.read_csv(score_save_path,index_col=[0,1])
    score_data.drop('is_churn',axis=1,inplace=True)

    binary_cols = [col for col in score_data if len(score_data[col].unique())==2]
    score_data.drop(binary_cols,axis=1,inplace=True)

    metric_columns = list(score_data.columns.values)

    labels = find_correlation_clusters(score_data.corr(),group_corr_thresh)
    labeled_column_df, relabled_count = relabel_clusters(labels,metric_columns)
    loadmat_df = make_load_matrix(labeled_column_df, metric_columns, relabled_count,group_corr_thresh)

    n_non_bin = loadmat_df.shape[1]
    n_bin = len(binary_cols)
    new_label_rows = pd.DataFrame(data=list(zip(range(n_non_bin,n_non_bin+n_bin),binary_cols)),
                                  columns=labeled_column_df.columns)
    labeled_column_df = labeled_column_df.append(new_label_rows)

    for c in binary_cols:
        loadmat_df[c]=0.0
    new_mat_rows = pd.DataFrame(data=0.0,index=binary_cols,columns=loadmat_df.columns)
    loadmat_df = loadmat_df.append(new_mat_rows)
    for c in binary_cols:
        loadmat_df.at[c,c]=1.0

    save_load_matrix(data_set_path,loadmat_df,labeled_column_df)
