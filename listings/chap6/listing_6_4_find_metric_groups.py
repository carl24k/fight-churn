import pandas as pd
import numpy as np
import os
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform


def find_correlation_clusters(corr,corr_thresh):
    dissimilarity = 1.0 - corr
    hierarchy = linkage(squareform(dissimilarity), method='single')
    diss_thresh = 1.0 - corr_thresh
    labels = fcluster(hierarchy, diss_thresh, criterion='distance')
    return labels

def relabel_clusters(labels,metric_columns):
    cluster_count = Counter(labels)
    cluster_order = {cluster[0]: idx for idx, cluster in enumerate(cluster_count.most_common())}
    relabeled_clusters = [cluster_order[l] for l in labels]
    relabled_count = Counter(relabeled_clusters)
    labeled_column_df = pd.DataFrame({'group': relabeled_clusters, 'column': metric_columns}).sort_values(
        ['group', 'column'], ascending=[True, True])
    return labeled_column_df, relabled_count

def make_load_matrix(labeled_column_df,metric_columns,relabled_count,corr):
    load_mat = np.zeros((len(metric_columns), len(relabled_count)))
    for row in labeled_column_df.iterrows():
        orig_col = metric_columns.index(row[1][1])
        if relabled_count[row[1][0]]>1:
            load_mat[orig_col, row[1][0]] = 1.0/  (np.sqrt(corr) * float(relabled_count[row[1][0]])  )
        else:
            load_mat[orig_col, row[1][0]] = 1.0

    is_group = load_mat.astype(bool).sum(axis=0) > 1
    column_names=['metric_group_{}'.format(d + 1) if is_group[d]
                      else labeled_column_df.loc[labeled_column_df['group']==d,'column'].iloc[0]
                      for d in range(0, load_mat.shape[1])]
    loadmat_df = pd.DataFrame(load_mat, index=metric_columns, columns=column_names)
    loadmat_df['name'] = loadmat_df.index
    sort_cols = list(loadmat_df.columns.values)
    sort_order = [False] * loadmat_df.shape[1]
    sort_order[-1] = True
    loadmat_df = loadmat_df.sort_values(sort_cols, ascending=sort_order)
    loadmat_df = loadmat_df.drop('name', axis=1)
    return loadmat_df

def save_load_matrix(data_set_path,loadmat_df, labeled_column_df):
    save_path = data_set_path.replace('.csv', '_load_mat.csv')
    print('saving loadings to ' + save_path)
    loadmat_df.to_csv(save_path)
    save_path = data_set_path.replace('.csv', '_groupmets.csv')
    print('saving metric groups to ' + save_path)
    group_lists=['|'.join(labeled_column_df[labeled_column_df['group']==g]['column'])
                    for g in set(labeled_column_df['group'])]
    pd.DataFrame(group_lists,index=loadmat_df.columns.values,columns=['metrics']).to_csv(save_path)

def find_metric_groups(data_set_path,group_corr_thresh=0.5):

    score_save_path=data_set_path.replace('.csv','_scores.csv')
    assert os.path.isfile(score_save_path),'You must run listing 5.3 or 7.5 to save metric scores first'
    score_data = pd.read_csv(score_save_path,index_col=[0,1])
    score_data.drop('is_churn',axis=1,inplace=True)
    metric_columns = list(score_data.columns.values)

    labels = find_correlation_clusters(score_data.corr(),group_corr_thresh)
    labeled_column_df, relabled_count = relabel_clusters(labels,metric_columns)
    loadmat_df = make_load_matrix(labeled_column_df, metric_columns, relabled_count,group_corr_thresh)
    save_load_matrix(data_set_path,loadmat_df,labeled_column_df)
