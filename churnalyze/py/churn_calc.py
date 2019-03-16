
import pandas as pd
import numpy as np


def behavioral_cohort_plot_data(churn_data, var_to_plot,out_col='is_churn'):
    sorted = churn_data.sort_values(by=var_to_plot)
    groups = pd.qcut(sorted[var_to_plot], 10, duplicates='drop')
    midpoints = sorted.groupby(groups)[var_to_plot].mean()
    churns = sorted.groupby(groups)[out_col].mean()
    plot_frame = pd.DataFrame({var_to_plot: midpoints.values, 'churn_rate': churns})

    return plot_frame


def dataset_stats(churn_data,metric_cols,save_path=None):
    
    summary=churn_data[metric_cols].describe()
    summary=summary.transpose()
    skew_stats=churn_data[metric_cols].skew()
    summary['skew']=skew_stats

    if save_path is not None:
        churn_stat=churn_data['is_churn'].astype(int).describe()
        churn_stat.to_csv(save_path+'_churnrate.csv',header=True)
        summary.to_csv(save_path+'_summary.csv',header=True)

    return summary


def normalize_skewscale(churn_data, plot_columns,summary, log_scale_skew_thresh=4):
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
