import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy import spatial, cluster

from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

import churn_calc as cc
from churn_const import save_path, key_cols, no_plot, schema_data_dict

# schema = 'b'
# schema = 'v'
schema = 'k'

data_file = schema_data_dict[schema]
schema_save_path = save_path(schema)+data_file


def main():
    churn_data = pd.read_csv(schema_save_path+'.csv',index_col=0)
    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    metric_cols = cc.churn_metric_columns(churn_data.columns.values)

    summary = cc.dataset_stats(churn_data,metric_cols)
    data_scores, skewed_columns = cc.normalize_skewscale(churn_data, metric_cols, summary)
    corr = data_scores[metric_cols].corr()
    print('Calculated correlation size %dx%d' % corr.shape)

    dissimilarity = 1.0 - corr
    hierarchy = linkage(squareform(dissimilarity), method='average')
    labels = fcluster(hierarchy, 0.5, criterion='distance')
    clusters = set(labels)
    print('%d clusters on %d variables' % (len(clusters), len(labels)))
    cluster_count=Counter(labels)
    cluster_order={cluster[0]:idx for idx,cluster in enumerate(cluster_count.most_common())}
    relabeled_clusters = [cluster_order[l] for l in labels]

    labeled_columns=pd.DataFrame({'group':relabeled_clusters, 'column':metric_cols}).sort_values(['group', 'column'],
                                                                                                 ascending=[True, True])

    ordered_corr=corr[labeled_columns.column].reindex(labeled_columns.column)


    ordered_corr.to_csv(schema_save_path + '_grouped_corr.csv')


if __name__ == "__main__":
    main()
