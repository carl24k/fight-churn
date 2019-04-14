
import pandas as pd
import numpy as np

from churn_const import out_col, no_plot, save_path, schema_data_dict, skip_metrics,key_cols,max_clips,min_valid

def data_load(schema):
    data_file = schema_data_dict[schema]
    schema_save_path = save_path(schema) + data_file
    churn_data = pd.read_csv(schema_save_path + '.csv')
    if data_file in skip_metrics:
        churn_data.drop(skip_metrics[data_file], axis=1,inplace=True)
    churn_data.set_index(key_cols,inplace=True)

    for metric in max_clips.keys():
        if metric in churn_data.columns.values:
            churn_data[metric].clip(upper=max_clips[metric], inplace=True)

    print('%s size before validation of columns: %d' % (data_file, churn_data.shape[0]))

    for metric in min_valid.keys():
        if metric.lower() in churn_data.columns.values:
            churn_data=churn_data[churn_data[metric.lower()]>min_valid[metric]]


    print('Loaded %s, size=%dx%d with columns:' % (data_file, churn_data.shape[0], churn_data.shape[1]))

    return churn_data

def behavioral_cohort_plot_data(churn_data, var_to_plot,nbin=10,out_col=out_col):
    """
    Make a data frame with two columns prepared to be the plot points for a behavioral cohort plot.
    The data is binned into 10 ordered bins, and the mean value of the metric and the churn rate are calculated
    for each bin.
    :param churn_data: Pandas data frame containing the data set
    :param var_to_plot: The variable to plot
    :param out_col:
    :return:
    """
    sorted = churn_data.sort_values(by=var_to_plot)
    groups = pd.qcut(sorted[var_to_plot], nbin, duplicates='drop')
    midpoints = sorted.groupby(groups)[var_to_plot].mean()
    churns = sorted.groupby(groups)[out_col].mean()
    plot_frame = pd.DataFrame({var_to_plot: midpoints.values, 'churn_rate': churns})

    return plot_frame


def dataset_stats(churn_data,metric_cols,save_path=None):
    """
    Take basic stats of the data set.  Saving it is optional.
    :param churn_data: Pandas data frame containing the data set
    :param metric_cols: Columns which are metrics (and will have stats taken)
    :param save_path: If specified, will save to this path plus an extension
    :return: 
    """
    
    summary=churn_data[metric_cols].describe()
    summary=summary.transpose()

    skew_stats=churn_data[metric_cols].skew()
    summary['skew']=skew_stats

    nonzero=churn_data.astype(bool).sum(axis=0)
    summary['nonzero']=nonzero / churn_data.shape[0]

    if save_path is not None:
        churn_stat=churn_data['is_churn'].astype(int).describe()
        churn_stat.to_csv(save_path+'_churnrate.csv',header=True)
        summary.to_csv(save_path+'_summary.csv',header=True)

    return summary


def normalize_skewscale(churn_data, plot_columns,summary, log_scale_skew_thresh=3):
    """
    Normalize metric columns of a data set, including logarithmic scaling for columns that have high skew.
    The churn column is just copied over.
    :param churn_data:Pandas data frame containing the data set
    :param plot_columns: Columns which are metrics (and will have stats taken)
    :param summary: A summary data frame from dataset_stats (optional)
    :param log_scale_skew_thresh: Threshold above which to apply the scaling transform
    :return: Data frame with the normalized columns and which columns received the log transform
    """
    if summary is None:
        summary = dataset_stats(churn_data,plot_columns)
    data_scores=churn_data[plot_columns].copy()
    skewed_columns=(summary['skew']>log_scale_skew_thresh) & (summary['min'] >= 0)
    for col,do_scale in skewed_columns.iteritems():
        if do_scale:
            data_scores[col]=np.log(1.0+data_scores[col])

    data_scores=(data_scores-data_scores.mean())/data_scores.std()
    data_scores['is_churn']=churn_data['is_churn']

    return data_scores, skewed_columns


def churn_metric_columns(df_columns,verbose=True):
    all_columns=list(df_columns)
    if verbose:
        print(all_columns)
    plot_columns = [c for c in all_columns if c not in no_plot]
    return plot_columns
