import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import churn_calc as cc
from churn_const import save_path, schema_data_dict, load_mat_file

one_plot = None
behave_group = False

schema = 'b'
# schema = 'v'
# schema = 'k'

one_plot='Ask_Success_Rate'

data_file = schema_data_dict[schema]
schema_save_path = save_path(schema)+data_file


def main():
    churn_data = pd.read_csv(schema_save_path+'.csv',index_col=0)
    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    plot_columns = cc.churn_metric_columns(churn_data.columns.values)

    if one_plot is not None and one_plot.lower() not in plot_columns:
        print('\n*** No metric %s in data set %s !!!' % (one_plot,data_file))
        exit(-1)

    summary = cc.dataset_stats(churn_data,plot_columns)
    data_scores, skewed_columns = cc.normalize_skewscale(churn_data, plot_columns, summary)

    if behave_group:
        load_mat_df = pd.read_csv(save_path(schema, load_mat_file),index_col=0)
        grouped_columns=['G%d' % d for d in range(0,load_mat_df.shape[1])]
        churn_data_reduced = pd.DataFrame(np.matmul(data_scores[plot_columns].to_numpy(), load_mat_df.to_numpy()),columns=grouped_columns)
        churn_data_reduced['is_churn']=churn_data['is_churn']
        churn_data = churn_data_reduced
        plot_columns = grouped_columns
        the_one_plot=None
        skewed_columns={c:False for c in plot_columns }
    else:
        the_one_plot=one_plot


    for var_to_plot in plot_columns:
        if the_one_plot is not None and var_to_plot!=the_one_plot.lower(): continue

        print('Plotting churn vs %s' % var_to_plot)

        plot_frame=cc.behavioral_cohort_plot_data(churn_data,var_to_plot)
        churn_plot_max = round(plot_frame['churn_rate'].max()*110.0)/100.0

        if behave_group or not skewed_columns[var_to_plot]:
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
