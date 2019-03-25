import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy import spatial, cluster

from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

import churn_calc as cc
from churn_const import save_path, key_cols, no_plot, schema_data_dict, load_mat_file

# schema = 'b'
schema = 'v'
# schema = 'k'

data_file = schema_data_dict[schema]
schema_save_path = save_path(schema)+data_file


def main():
    churn_data = pd.read_csv(schema_save_path+'.csv',index_col=0)
    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    metric_cols = cc.churn_metric_columns(churn_data.columns.values)

    summary = cc.dataset_stats(churn_data,metric_cols)
    data_scores, skewed_columns = cc.normalize_skewscale(churn_data, metric_cols, summary)
    data_scores = data_scores[metric_cols]
    corr = data_scores[metric_cols].corr()
    print('Calculated correlation size %dx%d' % corr.shape)

    dissimilarity = 1.0 - corr
    hierarchy = linkage(squareform(dissimilarity), method='single')
    labels = fcluster(hierarchy, 0.5, criterion='distance')
    clusters = set(labels)
    print('%d clusters on %d variables' % (len(clusters), len(labels)))
    cluster_count=Counter(labels)
    cluster_order={cluster[0]:idx for idx,cluster in enumerate(cluster_count.most_common())}
    relabeled_clusters = [cluster_order[l] for l in labels]
    relabeled_count=Counter(relabeled_clusters)

    labeled_columns=pd.DataFrame({'group':relabeled_clusters, 'column':metric_cols}).sort_values(['group', 'column'],
                                                                                                 ascending=[True, True])

    print('saving re-ordered correlation')
    ordered_corr=corr[labeled_columns.column].reindex(labeled_columns.column)
    ordered_corr.to_csv(schema_save_path + '_ordered_corr.csv')

    load_mat = np.zeros((len(metric_cols),len(clusters)))
    for row in labeled_columns.iterrows():
        orig_col=metric_cols.index(row[1][1])
        load_mat[orig_col, row[1][0]]= 1.0/np.sqrt(relabeled_count[row[1][0]])

    print('saving loadings')
    save_load_df = pd.DataFrame(load_mat,index=metric_cols,columns=[d for d in range(0,load_mat.shape[1])])
    save_load_df.to_csv(save_path(schema, load_mat_file))

    reduced_data = np.matmul(data_scores.to_numpy(), load_mat)

    print('saving reduced data correlation')
    reduced_corr =  np.corrcoef(np.transpose(reduced_data))
    np.savetxt(schema_save_path + '_reduced_corr.csv',reduced_corr,delimiter=',')

    # https: // stackoverflow.com / questions / 29394377 / minimum - of - numpy - array - ignoring - diagonal
    mask = np.ones(reduced_corr.shape, dtype=bool)
    np.fill_diagonal(mask, 0)
    max_corr = reduced_corr[mask].max()
    print('Max off-diagonal of reduced correlation: %f' % max_corr)


if __name__ == "__main__":
    main()
