import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


one_plot=None
# schema = 'b'
# data_file = 'BroadlyDataSet1'

# schema = 'v'
# data_file = 'VersatureDataSet1'

schema = 'k'
data_file='KlipfolioDataSet1'

# one_plot='account_tenure'

save_path = '../../../fight-churn-output/' + schema + '/'
log_scale_skew_thresh=4

key_cols = no_plot = ['account_id', 'observation_date']
out_col = 'is_churn'
no_plot.append(out_col)


def behavioral_cohort_plot_data(churn_data, var_to_plot):
    sorted = churn_data.sort_values(by=var_to_plot)
    groups = pd.qcut(sorted[var_to_plot], 10, duplicates='drop')
    midpoints = sorted.groupby(groups)[var_to_plot].mean()
    churns = sorted.groupby(groups)[out_col].mean()
    plot_frame = pd.DataFrame({var_to_plot: midpoints.values, 'churn_rate': churns})

    return plot_frame


def main():
    churn_data = pd.read_csv(save_path+data_file+'.csv',index_col=0)


    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    columns=list(churn_data.columns.values)
    print(columns)
    plot_columns=[c for c in columns if c not in no_plot]

    churn_stat=churn_data['is_churn'].astype(int).describe()
    churn_stat.to_csv(save_path+data_file+'_churnrate.csv',header=True)
    summary=churn_data[plot_columns].describe()
    summary=summary.transpose()
    skew_stats=churn_data[plot_columns].skew()
    summary['skew']=skew_stats
    summary.to_csv(save_path+data_file+'_summary.csv',header=True)

    data_scores=churn_data[plot_columns].copy()
    skewed_columns=(summary['skew']>log_scale_skew_thresh) & (summary['min']>=0)
    for col,do_scale in skewed_columns.iteritems():
        if do_scale: data_scores[col]=np.log(1.0+data_scores[col])

    data_scores=(data_scores-data_scores.mean())/data_scores.std()
    data_scores['is_churn']=churn_data['is_churn']

    for var_to_plot in plot_columns:
        if one_plot is not None and var_to_plot!=one_plot: continue

        print('Plotting churn vs %s' % var_to_plot)

        plot_frame=behavioral_cohort_plot_data(churn_data,var_to_plot)
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
            score_frame = behavioral_cohort_plot_data(data_scores, var_to_plot)
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
