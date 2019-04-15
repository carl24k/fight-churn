import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def cohort_plot(data_set_path, metric_to_plot,nbin=10):
    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    sorted = churn_data.sort_values(by=metric_to_plot)
    groups = pd.qcut(sorted[metric_to_plot], nbin, duplicates='drop')
    cohort_means = sorted.groupby(groups)[metric_to_plot].mean()
    cohort_churns = sorted.groupby(groups)[out_col].mean()
    plot_frame = pd.DataFrame({metric_to_plot: cohort_means.values, 'churn_rate': cohort_churns})
    plt.figure(figsize=(6, 4))
    plt.plot(metric_to_plot, 'churn_rate', data=plot_frame,marker='o', color='red', linewidth=2, label=metric_to_plot)
    plt.xlabel('Cohort Average of  "%s"' % metric_to_plot)
    plt.ylabel('Cohort Churn Rate (%)')
