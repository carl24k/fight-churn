import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
import  datetime

def event_count_plot(qa_data_path, event_name,**kwargs):
    qa_data_df=pd.read_csv(qa_data_path + '_' + event_name + '.csv')
    plt.figure(figsize=(6, 4))
    plt.plot('event_date', 'n_event', data=qa_data_df, marker='', color='black', linewidth=2)
    plt.ylim(0, ceil(1.1 * qa_data_df['n_event'].dropna().max()))
    plt.title('{} event count'.format(event_name))
    plt.gca().figure.autofmt_xdate()
    plt.xticks(list(filter(lambda x:x.endswith(("01")),qa_data_df['event_date'].tolist())))
    plt.tight_layout()
    plt.savefig(qa_data_path.replace('.csv', '_' + event_name + '_event_qa.png'))
    plt.close()
