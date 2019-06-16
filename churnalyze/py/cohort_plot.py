import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from math import ceil
from churn_calc import ChurnCalculator

font = {'family': 'Brandon Grotesque', 'size': 20}
matplotlib.rc('font', **font)

def plot_cohort_churn(cc,run_mets=None,hide_ax=False,always_score=False,behave_group=False):

    plot_columns = cc.churn_metric_columns()
    ax_scale=cc.get_conf('ax_scale')

    data_scores, skewed_columns = cc.normalize_skewscale()

    if always_score:
        skewed_columns={c:True for c in plot_columns }

    if behave_group:
        cc.group_behaviors()
        churn_data = cc.churn_data_reduced
        plot_columns = cc.grouped_columns
        the_one_plot=None
        skewed_columns={c:False for c in plot_columns }
    else:
        churn_data = cc.churn_data
        plot_columns = cc.metric_columns
        the_one_plot=[l.lower() for l in run_mets] if run_mets is not None else None


    for var_to_plot in plot_columns:
        if the_one_plot is not None and var_to_plot not in the_one_plot: continue

        print('Plotting churn vs %s' % var_to_plot)
        renames = cc.get_conf('renames')
        if var_to_plot not in renames:
            renames[var_to_plot]=var_to_plot

        plot_frame=cc.behavioral_cohort_plot_data(var_to_plot,nbin)
        bins_used=plot_frame.shape[0]
        bins_zero=nbin-bins_used
        churn_plot_max = ceil(plot_frame['churn_rate'].max()* ax_scale)/100.0

        if behave_group or not skewed_columns[var_to_plot]:
            plt.figure(figsize=(6,4))
            plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                     marker='o', color='red', linewidth=2, label=var_to_plot)
            plt.gcf().subplots_adjust(bottom=0.2)
            plt.xlabel('Cohort Average of  "%s"' % renames[var_to_plot])
            # plt.title('Churn vs. Cohorts of %s' % var_to_plot)
            plt.ylim(0, churn_plot_max)
            if hide_ax:
                plt.gca().get_yaxis().set_ticks([ 0.25*churn_plot_max, 0.5*churn_plot_max, 0.75*churn_plot_max, 1.0*churn_plot_max])
                plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
                plt.ylabel('Cohort Churn (Relative)')
            else:
                plt.ylabel('Cohort Churn Rate (%)')
            plt.grid()

        else:
            score_frame = cc.behavioral_cohort_plot_data(data_scores, var_to_plot,nbin=nbin)
            plt.figure(figsize=(10, 10))
            plt.subplot(2, 1, 1)
            plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                     marker='o', color='red', linewidth=2, label=var_to_plot)
            plt.ylabel('Cohort Churn Rate (%)')
            plt.xlabel('Cohort Average of  "%s"' % renames[var_to_plot])
            plt.grid()
            # plt.title('Churn vs. Cohorts of %s' % var_to_plot)
            plt.ylim(0, churn_plot_max)
            if hide_ax:
                plt.gca().get_yaxis().set_ticks([ 0.25*churn_plot_max, 0.5*churn_plot_max, 0.75*churn_plot_max, 1.0*churn_plot_max])
                plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
                plt.ylabel('Cohort Churn (Relative)')
            else:
                plt.ylabel('Cohort Churn Rate (%)')

            plt.subplot(2, 1, 2)
            plt.plot(var_to_plot, 'churn_rate', data=score_frame,
                     marker='o', color='blue', linewidth=2, label='score(%s)'%var_to_plot)
            plt.xlabel('Cohort Average of  "%s" (SCORE)' % renames[var_to_plot])
            plt.grid()
            plt.ylim(0, churn_plot_max)
            if hide_ax:
                plt.gca().get_yaxis().set_ticks([ 0.25*churn_plot_max, 0.5*churn_plot_max, 0.75*churn_plot_max, 1.0*churn_plot_max])
                plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
                plt.ylabel('Cohort Churn (Relative)')
            else:
                plt.ylabel('Cohort Churn Rate (%)')

        if hide_ax:
            save_name = 'churn_vs_' + var_to_plot + '_noax.png'
        else:
            save_name =  'churn_vs_' + var_to_plot + '.png'

        plt.savefig(cc.save_path(save_name,ext='png'))
        plt.close()


if __name__ == "__main__":

    schema = 'churnsim2'
    nbin = 10
    run_mets = None
    # Example of running just a few metrics - uncomment this line...
    # run_mets=['account_tenure','post_per_month']

    if len(sys.argv) >= 2:
        schema = sys.argv[1]
    if len(sys.argv) >3:
        nbin = int(sys.argv[2])
    if len(sys.argv) >= 4:
        run_mets = sys.argv[3:]

    churn_calc = ChurnCalculator(schema)
    plot_cohort_churn(churn_calc,run_mets)

