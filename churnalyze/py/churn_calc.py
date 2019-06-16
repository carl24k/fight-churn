import os
import pandas as pd
import numpy as np
import json


class ChurnCalculator:
    # misc constants set as class variables
    key_cols = ['account_id', 'observation_date']
    churn_out_col = 'is_churn'
    save_path_base = '../../../fight-churn-output/'
    load_mat_file = 'load_mat'
    no_plot_cols = list(key_cols)
    no_plot_cols.append(churn_out_col)

    def __init__(self, schema):
        self.schema = schema
        self.data_set_name = None
        self.churn_data = None
        with open('../conf/%s_churnalyze.json' % schema, 'r') as myfile:
            self.conf = json.loads(myfile.read())
        self.data_set_name = self.get_conf('dataset')
        self.data_load()
        # derived data created by calling functions
        self.summary = None
        self.data_scores = None
        self.skewed_columns = None
        self.churn_data_reduced = None
        self.reduced_cols = None

    def get_conf(self, name):
        if self.data_set_name is not None:
            if self.data_set_name in self.conf:
                if name in self.conf[self.data_set_name]:
                    return self.conf[self.data_set_name][name]
        if name in self.conf['default']:
            return self.conf['default'][name]
        return None

    def get_renames(self):
        renames=self.get_conf('renames')
        if isinstance(renames,dict) and len(renames)>0:
            orig_renames=list(renames.keys())
            for k in orig_renames:
                renames[k.lower()]=renames[k]
        return renames

    def data_load(self):
        data_set_path = self.save_path()
        self.churn_data = pd.read_csv(data_set_path)
        skip_metrics = self.get_conf('skip_metrics')
        if skip_metrics is not None and isinstance(skip_metrics,list) > 0:
            self.churn_data.drop(skip_metrics, axis=1, inplace=True)
        self.churn_data.set_index(self.key_cols, inplace=True)

        max_clips = self.get_conf('max_clips')
        if max_clips is not None and isinstance(max_clips, dict):
            for metric in max_clips.keys():
                if metric in self.churn_data.columns.values:
                    self.churn_data[metric].clip(upper=max_clips[metric], inplace=True)

        print('%s size before validation of columns: %d' % (self.data_set_name, self.churn_data.shape[0]))

        min_valid = self.get_conf('min_valid')
        if min_valid is not None and isinstance(min_valid, dict):
            for metric in min_valid.keys():
                if metric.lower() in self.churn_data.columns.values:
                    self.churn_data = self.churn_data[self.churn_data[metric.lower()] > min_valid[metric]]

        self.metric_columns = self.churn_metric_columns()
        self.metrics_plus_churn = list(self.metric_columns)
        self.metrics_plus_churn.append(self.churn_out_col)
        print('Loaded %s, size=%dx%d with columns:' % (
        self.data_set_name, self.churn_data.shape[0], self.churn_data.shape[1]))
        print('|'.join(self.metric_columns))

    def behavioral_cohort_plot_data(self, var_to_plot, use_score=False, nbin=10, out_col=churn_out_col):
        """
        Make a data frame with two columns prepared to be the plot points for a behavioral cohort plot.
        The data is binned into 10 ordered bins, and the mean value of the metric and the churn rate are calculated
        for each bin.
        :param var_to_plot: The variable to plot
        :param out_col:
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
        :param metric_cols: Columns which are metrics (and will have stats taken)
        :param save_path: If specified, will save to this path plus an extension
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

    def dataset_corr(self,use_scores=True,save=False):
        if use_scores:
            data,skew_cols = self.normalize_skewscale()
        else:
            data=self.churn_data[self.metrics_plus_churn]

        corr = data.corr()
        if save:
            corr.to_csv(self.save_path('corr'))


    def normalize_skewscale(self, log_scale_skew_thresh=4):
        """
        Normalize metric columns of a data set, including logarithmic scaling for columns that have high skew.
        The churn column is just copied over.
        :param plot_columns: Columns which are metrics (and will have stats taken)
        :param summary: A summary data frame from dataset_stats (optional)
        :param log_scale_skew_thresh: Threshold above which to apply the scaling transform
        :return: Data frame with the normalized columns and which columns received the log transform
        """
        if self.data_scores is None:
            self.dataset_stats()  # make sure summary is created
            self.data_scores = self.churn_data[self.metric_columns].copy()
            self.skewed_columns = (self.summary['skew'] > log_scale_skew_thresh) & (self.summary['min'] >= 0)
            for col, do_scale in self.skewed_columns.iteritems():
                if do_scale:
                    self.data_scores[col] = np.log(1.0 + self.data_scores[col])

            self.data_scores = (self.data_scores - self.data_scores.mean()) / self.data_scores.std()
            self.data_scores['is_churn'] = self.churn_data['is_churn']

        return self.data_scores, self.skewed_columns

    def churn_metric_columns(self):
        all_columns = list(self.churn_data.columns.values)
        plot_columns = [c for c in all_columns if c not in ChurnCalculator.no_plot_cols]
        return plot_columns

    def group_behaviors(self):

        self.normalize_skewscale()  # make sure scores are created

        load_mat_df = pd.read_csv(self.save_path(ChurnCalculator.load_mat_file), index_col=0)
        num_weights = load_mat_df.astype(bool).sum(axis=0)
        load_mat_df = load_mat_df.loc[:, num_weights > 1]
        grouped_columns = ['Metric Group %d' % (d + 1) for d in range(0, load_mat_df.shape[1])]
        self.churn_data_reduced = pd.DataFrame(
            np.matmul(self.data_scores[self.metric_columns].to_numpy(), load_mat_df.to_numpy()),
            columns=grouped_columns, index=self.churn_data.index)
        self.churn_data_reduced['is_churn'] = self.churn_data['is_churn']
        self.reduced_cols = grouped_columns

        # churn_data = churn_data_reduced
        # plot_columns = grouped_columns
        # the_one_plot = None
        # skewed_columns = {c: False for c in plot_columns}

    def save_path(self, file_name=None,ext='csv',subdir=None):
        save_path = ChurnCalculator.save_path_base + self.schema + '/'
        if subdir is not None:
            save_path += subdir + '/'
        os.makedirs(save_path, exist_ok=True)
        if self.data_set_name is None and file_name is not None:
            return save_path + '/' + file_name + '.' + ext
        elif file_name is  None and self.data_set_name is not None:
            return save_path + '/' + self.data_set_name + '.' + ext
        elif file_name is  not None and self.data_set_name is not None:
            return save_path + '/' + self.data_set_name + '_' + file_name + '.' + ext
        else:
            raise Exception("Must provide file name or previously set the datset ")
