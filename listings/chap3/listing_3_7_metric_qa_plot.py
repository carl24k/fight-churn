import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
import os

def metric_qa_plot(qa_data_path, metric_name,**kwargs):
    qa_data_df=pd.read_csv(qa_data_path)

    plt.figure(figsize=(8, 10))
    plt.subplot(4, 1, 1)
    plt.plot('calc_date', 'max', data=qa_data_df, marker='', color='black', linewidth=2, label="max")
    plt.ylim(0, ceil(1.1 * qa_data_df['max'].dropna().max()))
    plt.legend()
    plt.title(metric_name)
    plt.subplot(4, 1, 2)
    plt.plot('calc_date', 'avg', data=qa_data_df, marker='',linestyle='--', color='black', linewidth=2, label='avg')
    plt.ylim(0, ceil(1.1 * qa_data_df['avg'].dropna().max()))
    plt.legend()
    plt.subplot(4, 1, 3)
    plt.plot('calc_date', 'min', data=qa_data_df, marker='',linestyle='-.',  color='black', linewidth=2, label='min')
    plt.ylim(0, ceil(2*qa_data_df['min'].dropna().max()))
    plt.legend()
    plt.subplot(4, 1, 4)
    plt.plot('calc_date', 'n_calc', data=qa_data_df, marker='',linestyle=':',  color='black', linewidth=2, label="n_calc")
    plt.ylim(0, ceil(1.1 * qa_data_df['n_calc'].dropna().max()))
    plt.legend()
    plt.gca().figure.autofmt_xdate()

    plt.gcf().autofmt_xdate()

    plt.savefig(qa_data_path.replace('.csv', '_' + metric_name + '_churn_qa.png'))
    plt.close()
