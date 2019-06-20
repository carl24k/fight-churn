import pandas as pd
import matplotlib.pyplot as plt

def metric_pair_plot(data_set_path='', metric1='',metric2='',save_path='example.png'):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)

    met1_series = churn_data[metric1]
    met2_series = churn_data[metric2]

    corr = met1_series.corr(met2_series)

    plt.figure(figsize=(6, 6))
    plt.scatter(met1_series, met2_series, marker='.')
    plt.xlabel(metric1)
    plt.ylabel(metric2)
    plt.title('Correlation = %.2f' % corr)
    plt.tight_layout()
    plt.savefig(save_path)
    print('Saving plot to %s' % save_path)
    plt.close()
