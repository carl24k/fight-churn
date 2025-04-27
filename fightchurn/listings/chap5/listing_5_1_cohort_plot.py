import pandas as pd
import matplotlib.pyplot as plt
import os

def cohort_plot(data_set_path, metric_to_plot='',ncohort=10, exclude_zeros=False, log_scale=False):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    if exclude_zeros:
        churn_data = churn_data[churn_data[metric_to_plot]!=0]
    groups = pd.qcut(churn_data[metric_to_plot], ncohort, duplicates='drop')
    cohort_means = churn_data.groupby(groups, observed=False)[metric_to_plot].mean()
    cohort_churns = churn_data.groupby(groups, observed=False)['is_churn'].mean()
    plot_frame = pd.DataFrame({metric_to_plot: cohort_means.values, 'churn_rate': cohort_churns.values})
    plt.figure(figsize=(6, 4))
    plt.plot(metric_to_plot, 'churn_rate', data=plot_frame,marker='o', color='black', linewidth=2, label=metric_to_plot)
    plt.xlabel('Cohort Average of  "%s"' % metric_to_plot)
    plt.ylabel('Cohort Churn Rate')
    plt.grid()
    plt.gca().set_ylim(bottom=0)
    if log_scale:
        plt.gca().set_xscale('log')
    save_path = data_set_path.replace('.csv', '_' + metric_to_plot + '_churn_cohort.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)
    plt.close()
