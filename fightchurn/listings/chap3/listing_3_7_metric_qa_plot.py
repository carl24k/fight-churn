import pandas as pd
import matplotlib.pyplot as plt
from math import ceil

def metric_qa_plot(qa_data_path, metric_name,**kwargs):
    metric_data_path = qa_data_path + '_' + metric_name + '.csv'
    qa_data_df=pd.read_csv(metric_data_path)
    plt.figure(figsize=(6, 6))
    qa_subplot(qa_data_df,'max',1,None)
    plt.title(metric_name)
    qa_subplot(qa_data_df,'avg',2,'--')
    qa_subplot(qa_data_df,'min',3,'-.')
    qa_subplot(qa_data_df,'n_calc',4,':')
    plt.gca().figure.autofmt_xdate()
    save_to_path=metric_data_path.replace('.csv', '.png')
    print('Saving metric qa plot to ' + save_to_path)
    plt.savefig(save_to_path)
    plt.close()

def qa_subplot(qa_data_df, field, number, linestyle):
    plt.subplot(4, 1, number)
    plt.plot('calc_date', field, data=qa_data_df, marker='', linestyle=linestyle, color='black', linewidth=2, label=field)
    plt.ylim(0, ceil(1.1 * qa_data_df[field].dropna().max()))
    plt.legend()
