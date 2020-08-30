import pandas as pd
import matplotlib.pyplot as plt
import os

def cohort_plot_fixed(data_set_path, metric_to_plot='',cuts=None):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    purchase_data = pd.read_csv(data_set_path,index_col=[0,1])
    groups = pd.cut(purchase_data[metric_to_plot], cuts, duplicates='drop')
    cohort_means = purchase_data.groupby(groups)[metric_to_plot].mean()
    cohort_purchases = purchase_data.groupby(groups)['purchase'].mean()
    plot_frame = pd.DataFrame({metric_to_plot: cohort_means.values, 'purchase_rate': cohort_purchases})
    plt.figure(figsize=(6, 4))
    plt.plot(metric_to_plot, 'purchase_rate', data=plot_frame,marker='o', color='black', linewidth=2, label=metric_to_plot)
    plt.xlabel('Cohort Average of  "%s"' % metric_to_plot)
    plt.ylabel('Cohort purchase Rate')
    plt.grid()
    plt.gca().set_ylim(bottom=0)
    plt.gca().get_yaxis().set_ticklabels([])
    save_path = data_set_path.replace('.csv', '_' + metric_to_plot + '_purchase_corhort.png')
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)
