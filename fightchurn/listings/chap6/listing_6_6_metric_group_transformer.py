import os
import numpy as np
import pandas as pd
import joblib

from sklearn.base import BaseEstimator, TransformerMixin
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

class HeirarchicalClusterDimReducer( BaseEstimator, TransformerMixin ):

    def __init__( self, corr_thresh, out_col='is_churn'):
        self.corr_thresh = corr_thresh
        self.diss_thresh = 1.0 - corr_thresh # dissimilarity threshold
        self.out_col = out_col
        self.load_mat_df = None
        self.load_mat_ndarray = None
        self.metric_columns = None

    def reset_out_col(self,new_col=None):
        old_col = self.out_col
        self.out_col = None
        return old_col

    def _find_correlation_clusters(self, corr):
        dissimilarity = 1.0 - corr
        hierarchy = linkage(squareform(dissimilarity), method='single')
        labels = fcluster(hierarchy, self.diss_thresh, criterion='distance')
        return labels

    def _relabel_clusters(self, labels):
        cluster_count = Counter(labels)
        cluster_order = {cluster[0]: idx for idx, cluster in enumerate(cluster_count.most_common())}
        relabeled_clusters = [cluster_order[l] for l in labels]
        relabled_count = Counter(relabeled_clusters)
        labeled_column_df = pd.DataFrame({'group': relabeled_clusters, 'column': self.metric_columns}).sort_values(
            ['group', 'column'], ascending=[True, True])
        return labeled_column_df, relabled_count

    def _make_load_matrix(self, labeled_column_df, relabled_count):
        load_mat = np.zeros((len(self.metric_columns), len(relabled_count)))
        for row in labeled_column_df.iterrows():
            orig_col = self.metric_columns.index(row[1][1])
            if relabled_count[row[1][0]] > 1:
                load_mat[orig_col, row[1][0]] = 1.0 / (np.sqrt(self.corr_thresh) * float(relabled_count[row[1][0]]))
            else:
                load_mat[orig_col, row[1][0]] = 1.0

        is_group = load_mat.astype(bool).sum(axis=0) > 1
        column_names = ['metric_group_{}'.format(d + 1) if is_group[d]
                        else labeled_column_df.loc[labeled_column_df['group'] == d, 'column'].iloc[0]
                        for d in range(0, load_mat.shape[1])]
        loadmat_df = pd.DataFrame(load_mat, index=self.metric_columns, columns=column_names)
        loadmat_df['name'] = loadmat_df.index
        sort_cols = list(loadmat_df.columns.values)
        sort_order = [False] * loadmat_df.shape[1]
        sort_order[-1] = True
        loadmat_df = loadmat_df.sort_values(sort_cols, ascending=sort_order)
        loadmat_df = loadmat_df.drop('name', axis=1)
        return loadmat_df

    def _drop_outcome(self,X, return_outcome=False):
        if self.out_col is not None:
            data_to_fit = X.drop(self.out_col,axis=1)
            out = X[self.out_col]
        else:
            data_to_fit = X
            out = None
        if not return_outcome:
            return data_to_fit
        else:
            return data_to_fit, out

    def fit( self, X, y = None ):
        data_to_fit = self._drop_outcome(X)
        self.metric_columns = list(data_to_fit.columns.values)
        corr_matt = data_to_fit.corr()
        labels = self._find_correlation_clusters(corr_matt)
        labeled_column_df, relabled_count = self._relabel_clusters(labels)
        self.load_mat_df = self._make_load_matrix(labeled_column_df, relabled_count)
        self.load_mat_ndarray = self.load_mat_df.to_numpy()

    def transform( self, X, y = None ):
        data_to_fit, outcome = self._drop_outcome(X, return_outcome=True)

        ndarray_2group = data_to_fit[self.load_mat_df.index.values].to_numpy()
        grouped_ndarray = np.matmul(ndarray_2group, self.load_mat_ndarray)

        churn_data_grouped = pd.DataFrame(grouped_ndarray, columns=self.load_mat_df.columns.values, index=data_to_fit.index)

        if self.out_col is not None:
            churn_data_grouped[self.out_col] = outcome
        return churn_data_grouped



def metric_group_transformer(data_set_path,group_corr_thresh=0.5):

    score_save_path=data_set_path.replace('.csv','_scores.csv')
    assert os.path.isfile(score_save_path),'You must run listing 5.3 or 7.5 to save metric scores first'
    score_data = pd.read_csv(score_save_path,index_col=[0,1])

    transformer = HeirarchicalClusterDimReducer(group_corr_thresh)

    transformer.fit(score_data)

    reduced_data = transformer.transform(score_data)

    save_path = data_set_path.replace('.csv', '_groupscore.csv')
    reduced_data.to_csv(save_path,header=True)
    print('Saved grouped data  to ' + save_path)

    transformer_save_path=data_set_path.replace('.csv','_hc_dimreduce_transform.pkl')
    print('Saving fit Transformer to %s' % transformer_save_path)
    joblib.dump(transformer, transformer_save_path)