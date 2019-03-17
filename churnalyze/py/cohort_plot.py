import pandas as pd
import matplotlib.pyplot as plt

import churn_calc as cc
from churn_const import save_path, schema_data_dict

one_plot=None

# schema = 'b'
schema = 'v'
# schema = 'k'

one_plot='account_tenure'

data_file = schema_data_dict[schema]
schema_save_path = save_path(schema)+data_file


def main():
    churn_data = pd.read_csv(schema_save_path+'.csv',index_col=0)
    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    plot_columns = cc.churn_metric_columns(churn_data.columns.values)

    summary = cc.dataset_stats(churn_data,plot_columns)

    data_scores, skewed_columns = cc.normalize_skewscale(churn_data, plot_columns, summary)

    for var_to_plot in plot_columns:
        if one_plot is not None and var_to_plot!=one_plot: continue

        print('Plotting churn vs %s' % var_to_plot)

        plot_frame=cc.behavioral_cohort_plot_data(churn_data,var_to_plot)
        churn_plot_max = round(plot_frame['churn_rate'].max()*110.0)/100.0

        if not skewed_columns[var_to_plot]:
            plt.figure(figsize=(4,6))
            plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                     marker='o', color='red', linewidth=2, label=var_to_plot)
            plt.title('Churn vs. Cohorts of %s' % var_to_plot)
            plt.legend()
            plt.ylabel('Cohort churn rate')
            plt.ylim(0, churn_plot_max)
        else:
            score_frame = cc.behavioral_cohort_plot_data(data_scores, var_to_plot)
            plt.figure(figsize=(8, 10))
            plt.subplot(2, 1, 1)
            plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                     marker='o', color='red', linewidth=2, label=var_to_plot)
            plt.legend()
            plt.ylabel('Cohort churn rate')
            plt.xlabel('Cohort %s : Average Value' % var_to_plot)
            plt.title('Churn vs. Cohorts of %s' % var_to_plot)
            plt.ylim(0, churn_plot_max)

            plt.subplot(2, 1, 2)
            plt.plot(var_to_plot, 'churn_rate', data=score_frame,
                     marker='o', color='blue', linewidth=2, label='score(%s)'%var_to_plot)
            plt.legend()
            plt.ylabel('Cohort churn rate')
            plt.xlabel('Cohort %s Average Score' % var_to_plot)
            plt.ylim(0, churn_plot_max)

        plt.savefig(schema_save_path + 'churn_vs_' + var_to_plot + '.png')
        plt.close()


if __name__ == "__main__":
    main()
