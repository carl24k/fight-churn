import os
import pandas as pd
import numpy as np

from churn_const import out_col, no_plot, save_path, schema_data_dict, skip_metrics,key_cols,max_clips,min_valid

class ChurnCalculator:

    def __init__(self,schema):
        self.schema=schema
        self.churn_data=None
        self.data_load()
        self.metric_columns=self.churn_metric_columns()
        # derived data created by calling functions
        self.summary=None
        self.data_scores=None
        self.skewed_columns=None
        self.churn_data_reduced=None
        self.reduced_cols=None

        # misc constants set as member variables
        self.key_cols = ['account_id', 'observation_date']
        self.out_col = 'is_churn'
        self.no_plot = list(key_cols)
        self.no_plot.append(out_col)
        self.save_path_base = '../../../fight-churn-output/'
        self.load_mat_file = 'load_mat'

    def data_load(self):
        data_file = schema_data_dict[self.schema]
        schema_save_path = save_path(self.schema) + data_file
        self.churn_data = pd.read_csv(schema_save_path + '.csv')
        if data_file in skip_metrics:
            self.churn_data.drop(skip_metrics[data_file], axis=1,inplace=True)
        self.churn_data.set_index(key_cols,inplace=True)

        for metric in max_clips.keys():
            if metric in self.churn_data.columns.values:
                self.churn_data[metric].clip(upper=max_clips[metric], inplace=True)

        print('%s size before validation of columns: %d' % (data_file, self.churn_data.shape[0]))

        for metric in min_valid.keys():
            if metric.lower() in self.churn_data.columns.values:
                self.churn_data=self.churn_data[self.churn_data[metric.lower()]>min_valid[metric]]

        print('Loaded %s, size=%dx%d with columns:' % (data_file, self.churn_data.shape[0], self.churn_data.shape[1]))


    def behavioral_cohort_plot_data(self,var_to_plot,nbin=10,out_col=out_col):
        """
        Make a data frame with two columns prepared to be the plot points for a behavioral cohort plot.
        The data is binned into 10 ordered bins, and the mean value of the metric and the churn rate are calculated
        for each bin.
        :param var_to_plot: The variable to plot
        :param out_col:
        :return:
        """

        groups = pd.qcut(self.churn_data[var_to_plot], nbin, duplicates='drop')
        midpoints = self.churn_data.groupby(groups)[var_to_plot].mean()
        churns = self.churn_data.groupby(groups)[out_col].mean()
        plot_frame = pd.DataFrame({var_to_plot: midpoints.values, 'churn_rate': churns})

        return plot_frame


    def dataset_stats(self,save_path=None):
        """
        Take basic stats of the data set.  Saving it is optional.
        :param metric_cols: Columns which are metrics (and will have stats taken)
        :param save_path: If specified, will save to this path plus an extension
        :return:
        """

        if self.summary is None:

            self.summary=self.churn_data[self.metric_cols].describe()
            self.summary=self.summary.transpose()

            self.summary['skew'] = self.churn_data.skew()
            self.summary['1%'] = self.churn_data.quantile(q=0.01)
            self.summary['5%'] = self.churn_data.quantile(q=0.05)
            self.summary['10%'] = self.churn_data.quantile(q=0.10)
            self.summary['90%'] = self.churn_data.quantile(q=0.90)
            self.summary['95%'] = self.churn_data.quantile(q=0.95)
            self.summary['99%'] = self.churn_data.quantile(q=0.99)
            self.summary['nonzero'] = self.churn_data.astype(bool).sum(axis=0) / self.churn_data.shape[0]

            self.summary = self.summary[ ['count','nonzero','mean','std','skew','min','1%','5%','10%','25%','50%','75%','90%','95%','99%','max'] ]

        if save_path is not None:
            # Adding churn % stats in a saved version, but not for further analysis
            churn_stat=self.churn_data['is_churn'].astype(int).describe()
            churn_stat.to_csv(save_path+'_churnrate.csv',header=True)
            self.summary.to_csv(save_path+'_summary.csv',header=True)

        return self.summary


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
            self.dataset_stats() # make sure summary is created
            self.data_scores=self.churn_data[self.metric_columns].copy()
            skewed_columns=(self.summary['skew']>log_scale_skew_thresh) & (self.summary['min'] >= 0)
            for col,do_scale in skewed_columns.iteritems():
                if do_scale:
                    self.data_scores[col]=np.log(1.0+self.data_scores[col])

            self.data_scores=(self.data_scores-self.data_scores.mean())/self.data_scores.std()
            self.data_scores['is_churn']=self.churn_data['is_churn']

        return self.data_scores, self.skewed_columns


    def churn_metric_columns(self):
        all_columns=list(self.hurn_data.columns.values)
        plot_columns = [c for c in all_columns if c not in no_plot]
        return plot_columns

    def group_behaviors(self):

        self.normalize_skewscale() # make sure scores are created

        load_mat_df = pd.read_csv(save_path(self.schema, self.load_mat_file), index_col=0)
        num_weights = load_mat_df.astype(bool).sum(axis=0)
        load_mat_df = load_mat_df.loc[:, num_weights > 1]
        grouped_columns = ['Metric Group %d' % (d + 1) for d in range(0, load_mat_df.shape[1])]
        self.churn_data_reduced = pd.DataFrame(np.matmul(self.data_scores[self.metric_columns].to_numpy(), load_mat_df.to_numpy()),
                                          columns=grouped_columns, index=self.churn_data.index)
        self.churn_data_reduced['is_churn'] = self.churn_data['is_churn']
        self.reduced_cols=grouped_columns

        # churn_data = churn_data_reduced
        # plot_columns = grouped_columns
        # the_one_plot = None
        # skewed_columns = {c: False for c in plot_columns}

    def save_path(self,file_name=None):
        save_path=self.save_path_base + self.schema + '/'
        os.makedirs(save_path, exist_ok=True)
        if file_name is None:
            return save_path
        else:
            return save_path + '/' + schema_data_dict[self.schema] + '_' + file_name + '.csv'
