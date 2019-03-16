import pandas as pd
import matplotlib.pyplot as plt

import churn_calc as cc

one_plot=None

# schema = 'b'
# data_file = 'BroadlyDataSet1'

schema = 'v'
data_file = 'VersatureDataSet1'

# schema = 'k'
# data_file='KlipfolioDataSet1'

# one_plot='account_tenure'

save_path = '../../../fight-churn-output/' + schema + '/'
log_scale_skew_thresh=4

key_cols = no_plot = ['account_id', 'observation_date']
out_col = 'is_churn'
no_plot.append(out_col)


def main():
    churn_data = pd.read_csv(save_path+data_file+'.csv',index_col=0)

    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    columns=list(churn_data.columns.values)
    print(columns)
    plot_columns=[c for c in columns if c not in no_plot]

    summary = cc.dataset_stats(churn_data,plot_columns,save_path=save_path+data_file)

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

        plt.savefig(save_path + 'churn_vs_' + var_to_plot + '.png')
        plt.close()


if __name__ == "__main__":
    main()
