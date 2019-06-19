import os
import pandas as pd
import numpy as np
import json

# for the behavioral grouping
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform


class ChurnCalculator:
    '''
    Object that performs a variety a churn analysis calculations. It encapsulates all the operations for one schema
    and data set. The schema is the data universe that generated the data set which could be either a company, a product,
     or a simulated data set. If this is run as in the book Fighting  Churn With Data this would be the name of the
     database schema.

     For each schema there must be a configuration file in the adjacent directory named <schema>_churnalyze.json.
     See examples and the repository ReadMe for details on what has to go in the configuration, and the member function
     get_conf for access to the configuration contents in the code.

     The general process is to create a churn calculator which loads a data set, and then call member functions to
     do the various analytic tasks. The churn calculator saves csv files of results, but does not make plots - plotting
     is done in the various executable functions that use the ChurnCalculator.

     There is no main function in this file - there are main functions in all of the other files in this folder (and
     some of them are quite simple - they create the ChurnCalculator, call a function and exit. Others have a bit more
     content, particularly when it involves generating plots.)
    '''
    # misc constants set as class variables
    key_cols = ['account_id', 'observation_date']
    churn_out_col = 'is_churn'
    save_path_base = '../../../fight-churn-output/'
    load_mat_file = 'load_mat'
    no_plot_cols = list(key_cols)
    no_plot_cols.append(churn_out_col)

    def __init__(self, schema):
        '''
        Opens the Json configuration and gets the name of the default dataset, and loads that data set.
        Also sets None for the various analytic result objects.
        :param schema: The name for the universe of data.
        '''
        self.schema = schema
        self.data_set_name = None
        self.churn_data = None
        # Open the configuration
        with open('../conf/%s_churnalyze.json' % schema, 'r') as myfile:
            self.conf = json.loads(myfile.read())
        self.data_load(self.get_conf('dataset'))
        # derived data created by calling functions
        self.summary = None
        self.data_scores = None
        self.skewed_columns = None
        self.churn_data_reduced = None
        self.reduced_cols = None

    def get_conf(self, name, default=None):
        '''
        Retrieves one param from the configuration. If there is a dataset already set then it will look for the param
        in the json member for the dataset and return it if found.  Otherwise it looks in the 'default' entry.
        (So don't name your dataset "default")
        :param name: key for the configuration. assumed to be a string
        :return:
        '''
        if self.data_set_name is not None:
            if self.data_set_name in self.conf:
                if name in self.conf[self.data_set_name]:
                    return self.conf[self.data_set_name][name]
        if name in self.conf['default']:
            return self.conf['default'][name]
        return default

    def get_renames(self):
        '''
        Renaming utility for metrics to make more re-usable versions for the plots. There has to be an entry named
        "renames" in the configuration, and presumable it would be in the default configuration (although it is possible
        to have different dataset specific versions.) The renamings are simple string : string pairs where the key
        is the metric column name produced in the dataset, and the value is the desired string to appear in plots and
        graphs.

        By default every entry in the renaming is duplicated if necessary with a lower case version, so you
        can put cased versions in the configuration (possibly copied from imported event types) and it will still work
        with lower cased data frame column names.  Producing those entries is the task of this function, apart from
        simply loading the configuration.
        :return:
        '''
        renames=self.get_conf('renames')
        if isinstance(renames,dict) and len(renames)>0:
            orig_renames=list(renames.keys())
            for k in orig_renames:
                renames[k.lower()]=renames[k]
        return renames

    def data_load(self,new_data_set):
        '''
        Loads the data set from a file - the member variable is set and then save_path with no parameters returns the
        data file path. After loading the index is set to two column primary key (account id and observation date.)
        There are also some other functions performed based on settings in the configuration:
        1. Skip metrics: any metrics listed in the skip_metrics configuration are dropped
        2. max_clips: if metrics are specified with a maximum value to clip, the clipping is applied.
        3. min_valid: if min_valid values for metrics are specified, those observations failing the test are removed

        Note: After the skipping, two member variables "metric_columns" and "metric_columns_plus_churn" are set that
        contain lists of the columns being used.
        :return:
        '''
        self.data_set_name=new_data_set
        data_set_path = self.save_path()
        self.churn_data = pd.read_csv(data_set_path)
        self.churn_data.set_index(self.key_cols, inplace=True)

        skip_metrics = self.get_conf('skip_metrics')
        if skip_metrics is not None and isinstance(skip_metrics,list) > 0:
            self.churn_data.drop(skip_metrics, axis=1, inplace=True)

        # After skipping, set the lists of columns that are currently used
        self.metric_columns = self.churn_metric_columns()
        self.metrics_plus_churn = list(self.metric_columns)
        self.metrics_plus_churn.append(self.churn_out_col)

        # Clipping, if any is specified
        max_clips = self.get_conf('max_clips')
        if max_clips is not None and isinstance(max_clips, dict):
            for metric in max_clips.keys():
                if metric in self.churn_data.columns.values:
                    self.churn_data[metric].clip(upper=max_clips[metric], inplace=True)

        print('%s size before validation of columns: %d' % (self.data_set_name, self.churn_data.shape[0]))

        # Validation accoring to minimum values if any is specified
        min_valid = self.get_conf('min_valid')
        if min_valid is not None and isinstance(min_valid, dict):
            for metric in min_valid.keys():
                if metric.lower() in self.churn_data.columns.values:
                    self.churn_data = self.churn_data[self.churn_data[metric.lower()] > min_valid[metric]]

        # Print out the final status
        print('Loaded %s, size=%dx%d with columns:' % (
        self.data_set_name, self.churn_data.shape[0], self.churn_data.shape[1]))
        print('|'.join(self.metric_columns))

    def behavioral_cohort_plot_data(self, var_to_plot, use_score=False, nbin=10, out_col=churn_out_col):
        """
        Make a data frame with two columns prepared to be the plot points for a behavioral cohort plot.
        The data is binned into ordered bins with pcqut, and the mean value of the metric and the churn rate
        are calculated for each bin with the groupby function. The result is returned in a data frame.
        :param var_to_plot: The variable to plot
        :param use_score: Use the scored version of the data
        :param nbin: Number of cohorts
        :param out_col: the outcome, presumably churn
        :return:
        """
        if not use_score:
            data=self.churn_data
        else:
            data,_=self.normalize_skewscale()

        groups = pd.qcut(data[var_to_plot], nbin, duplicates='drop')
        midpoints = data.groupby(groups)[var_to_plot].mean()
        churns = data.groupby(groups)[out_col].mean()
        plot_frame = pd.DataFrame({var_to_plot: midpoints.values, 'churn_rate': churns})

        return plot_frame

    def dataset_stats(self, save=False):
        """
        Take basic stats of the data set.  Saving it is optional.
        :param save: If specified, will save to this path plus an extension
        :return:
        """

        if self.summary is None:
            self.summary = self.churn_data[self.metric_columns].describe()
            self.summary = self.summary.transpose()

            self.summary['skew'] = self.churn_data.skew()
            self.summary['1%'] = self.churn_data.quantile(q=0.01)
            self.summary['5%'] = self.churn_data.quantile(q=0.05)
            self.summary['10%'] = self.churn_data.quantile(q=0.10)
            self.summary['90%'] = self.churn_data.quantile(q=0.90)
            self.summary['95%'] = self.churn_data.quantile(q=0.95)
            self.summary['99%'] = self.churn_data.quantile(q=0.99)
            self.summary['nonzero'] = self.churn_data.astype(bool).sum(axis=0) / self.churn_data.shape[0]

            self.summary = self.summary[
                ['count', 'nonzero', 'mean', 'std', 'skew', 'min', '1%', '5%', '10%', '25%', '50%', '75%', '90%', '95%',
                 '99%', 'max']]

        if save:
            # Adding churn % stats in a saved version, but not for further analysis
            churn_stat = self.churn_data['is_churn'].astype(int).describe()
            churn_stat.to_csv(self.save_path('churnrate'), header=True)
            self.summary.to_csv(self.save_path('summary'), header=True)
            print('Saved result to ' + self.save_path('summary'))

        return self.summary

    def churn_rate(self):
        self.dataset_stats() # make sure the churn stat is calculated
        return self.churn_stat['mean']

    def dataset_corr(self,use_scores=True,save=False):
        '''
        Calculate a correlation matrix on the current data set. Optionally use the scored version of the data.
        If the save flag is set, the churn variable is saved so you can see correlation with churn. But if not saving
        churn is not included, since it is assumed this is the correlation matrix for behavioral grouping.
        :param use_scores: use the scores
        :param save: save it to a csv, and you are then include the churn variable
        :return: The correlation, as a panda data frame
        '''
        if use_scores:
            data,_ = self.normalize_skewscale()
            if not save:
                data=data.drop(self.churn_out_col,axis=1)
        elif save:
            data=self.churn_data[self.metrics_plus_churn]
        else:
            data=self.churn_data[self.metric_columns]

        corr = data.corr()

        if save:
            save_name = 'corr'
            if use_scores:
                save_name += '_scores'
            full_save_path = self.save_path(save_name)
            print('Saving result to ' + full_save_path)
            corr.to_csv(full_save_path)

        return corr

    def normalize_skewscale(self, log_scale_skew_thresh=4):
        """
        Normalize metric columns of a data set, including logarithmic scaling for columns that have high skew.
        After logarithmic scaling, the normal approach to standardization is taken: substract the man and divide
        by the standard deviation. The churn column is just copied over at the end.
        :param log_scale_skew_thresh: Threshold above which to apply the scaling transform
        :return: The correlation, as a panda data frame. Also a Series of boolean which indicates which columns were
        skewed above the threshold.
        """
        if self.data_scores is None:
            self.dataset_stats()  # make sure summary is already created
            self.data_scores = self.churn_data[self.metric_columns].copy()
            self.skewed_columns = (self.summary['skew'] > log_scale_skew_thresh) & (self.summary['min'] >= 0)
            for col, do_scale in self.skewed_columns.iteritems():
                if do_scale:
                    self.data_scores[col] = np.log(1.0 + self.data_scores[col])

            self.data_scores = (self.data_scores - self.data_scores.mean()) / self.data_scores.std()
            self.data_scores['is_churn'] = self.churn_data['is_churn']

        return self.data_scores, self.skewed_columns

    def churn_metric_columns(self):
        '''
        Helper function to take all the columns in the loaded data frame and remove the ones that are not metrics
        :return: The list of columns
        '''
        all_columns = list(self.churn_data.columns.values)
        plot_columns = [c for c in all_columns if c not in ChurnCalculator.no_plot_cols]
        return plot_columns

    def calc_behavior_groups(self):
        '''
        Calculate groupings for correlated behaviors based on heirarchical clustering.  This scipy functions:
        linkage and fcluster to do the actual clustering, so most of this code is concerned with reformatting the output
        into a weight matrix (loading matrix) that can be used to perform dimension reduction on the dataset.

        There are no parameters or return values - this operates on the preloaded member variables and and saves the
        results in files, in particular the loading matrix. Other results saved for inspection are a re-ordered version
        of the correlation matrix and the correlation matrix of the dimension reduced data set.

        The process is as follows:
        1. Get the correlation. The clustering works in terms of dissimilarity, so use 1.0 minus the correlation
        2. squareform reformats the dissimilarity matrix into the vector form required for linkage
        3. the linkage function returns a heirarchy based on the correlation matrix which is a representation of which
            elements are closest to each other, using the dissimilarity as distances.
        4. The threshold for a cluster is also set as a correlation (more intuitive) so the threshold for the clustering
            is 1.0 minus thethreshold
        5. fcluster decides on the cluster using the previously calculated heirarchy, and the specified threshold.
            fcluster. fcluster returns a series which are the class labels for each column as an ndarray

        The above completes the clustering.  The remainder is processing and reformatting the output.
        6. At this point it is not known how many clusters there are, so a set is created to find the unique elements
        7. A Counter is used to calculate the number of elements in each cluster
        8. A dictionary is made from the original cluster labels to their position in the new order user the Counter
            objects most_common method. A counter based on the relabeled clusters is also created for later use
        9. To faciliate construction of the weight matrix a two column data frame is created listing the mapping of the
            metric column names to the final (reordered) cluster assignments - named "labeled_columns"
        10. The weight matrix is created as a numpy zero matrix and then filled in by looking up the elements in the
            labeled_columns
            KEY STEP: Using the relabled_count to make the entries the appropriate sum of squares weight.
        11. After construction, the weight matrix is converted to a data frame with the column name as the index
            The group entries are in the columns.
        12. After creation, the loading matrix is sorted by the clustering and the metric names for readability
        :return:
        '''

        # This actually calculates the clusters
        corr = self.dataset_corr()
        dissimilarity = 1.0 - corr
        hierarchy = linkage(squareform(dissimilarity), method='single')
        thresh = 1.0 - self.get_conf('group_corr_thresh')
        labels = fcluster(hierarchy, thresh, criterion='distance')
        clusters = set(labels) # The unique list of the group labels

        # Relabel the clusters so the cluster with the most columns is first
        cluster_count = Counter(labels)
        cluster_order = {cluster[0]: idx for idx, cluster in enumerate(cluster_count.most_common())}
        relabeled_clusters = [cluster_order[l] for l in labels]
        relabeled_count = Counter(relabeled_clusters)

        labeled_columns = pd.DataFrame({'group': relabeled_clusters, 'column': self.metric_columns}).sort_values(
            ['group', 'column'],
            ascending=[True, True])

        load_mat = np.zeros((len(self.metric_columns), len(clusters)))
        for row in labeled_columns.iterrows():
            orig_col = self.metric_columns.index(row[1][1])
            load_mat[orig_col, row[1][0]] = 1.0 / np.sqrt(relabeled_count[row[1][0]])

        loadmat_df = pd.DataFrame(load_mat, index=self.metric_columns, columns=[d for d in range(0, load_mat.shape[1])])
        loadmat_df['name'] = loadmat_df.index
        sort_cols = list(loadmat_df.columns.values)
        sort_order = [False] * loadmat_df.shape[1]
        sort_order[-1] = True
        loadmat_df = loadmat_df.sort_values(sort_cols, ascending=sort_order)

        print('saving loadings')
        loadmat_df = loadmat_df.drop('name', axis=1)
        loadmat_df.to_csv(self.save_path(self.load_mat_file))

        print('saving re-ordered correlation')
        ordered_corr = corr[labeled_columns.column].reindex(labeled_columns.column)
        ordered_corr.to_csv(self.save_path('ordered_corr'))

        print('saving reduced data correlation')
        self.apply_behavior_grouping()
        reduced_corr = self.churn_data_reduced.corr()
        reduced_corr.to_csv(self.save_path('reduced_corr'))

    def apply_behavior_grouping(self):
        '''
        Produce a reduced version of the data by applying a previously saved weight matrix. This has to be applied to
        the normalized data, so that is created (if that has not already happened on this invocation.) Results are
        saved in member variables for use by other functions, for example cohort plotting.
        :return:
        '''

        self.normalize_skewscale()  # make sure scores are created
        # Load the previously saved loading matrix, created by
        load_mat_df = pd.read_csv(self.save_path(ChurnCalculator.load_mat_file), index_col=0)
        num_weights = load_mat_df.astype(bool).sum(axis=0)
        load_mat_df = load_mat_df.loc[:, num_weights > 1]
        grouped_columns = ['Metric Group %d' % (d + 1) for d in range(0, load_mat_df.shape[1])]
        self.churn_data_reduced = pd.DataFrame(
            np.matmul(self.data_scores[self.metric_columns].to_numpy(), load_mat_df.to_numpy()),
            columns=grouped_columns, index=self.churn_data.index)
        self.churn_data_reduced['is_churn'] = self.churn_data['is_churn']
        self.reduced_cols = grouped_columns


    def save_path(self, file_name=None,ext='csv',subdir=None):
        '''
        Makes a path from the schema and dataset to save the various
        outputs from the code
        :param file_name:
        :param ext:
        :param subdir:
        :return:
        '''
        save_path = ChurnCalculator.save_path_base + self.schema + '/'
        if subdir is not None:
            save_path += subdir + '/'
        os.makedirs(save_path, exist_ok=True)
        if self.data_set_name is None and file_name is not None:
            return save_path  + file_name + '.' + ext
        elif file_name is  None and self.data_set_name is not None:
            return save_path  + self.data_set_name + '.' + ext
        elif file_name is  not None and self.data_set_name is not None:
            return save_path  + self.data_set_name + '_' + file_name + '.' + ext
        else:
            raise Exception("Must provide file name or previously set the datset ")
