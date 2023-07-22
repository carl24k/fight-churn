import pandas as pd
import matplotlib.pyplot as plt
import os

def metric_histogram(data_set_path, bins=None, metric_to_plot='',limits=[],log_x=False, log_y=False):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])
    plt.figure(figsize=(6, 4))
    plt.hist(churn_data[metric_to_plot],bins=bins)
    if limits:
        plt.xlim(limits)
    if log_x:
        plt.gca().set_xscale('log')
    if log_y:
        plt.gca().set_yscale('log')
    plt.title(metric_to_plot)
    plt.xlabel(f'mean={churn_data[metric_to_plot].mean():.0f}, '
               f'max={churn_data[metric_to_plot].max():.0f}, '
               f'skew={churn_data[metric_to_plot].skew():.1f}')
    plt.ylabel('# of Observations')
    plt.tight_layout()
    plt.grid()
    save_path = data_set_path.replace('.csv', '_' + metric_to_plot + '_histogram.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)