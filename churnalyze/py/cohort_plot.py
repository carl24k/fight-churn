import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from math import ceil
import argparse

from churn_calc import ChurnCalculator


parser = argparse.ArgumentParser()
# Main run control arguments
parser.add_argument("--schema", type=str, help="The name of the schema", default='churnsim2')
parser.add_argument("--nbin", type=int, help="The number of bins",default=10)
parser.add_argument("--metrics", type=str,nargs='*', help="List of metrics to run (default to all)")
# Additional options
parser.add_argument("--hide_ax", action="store_true", default=False,help="Hide axis labeling for publication of case studies")
parser.add_argument("--always_score", action="store_true", default=False,help="Plot cohorts using scored metrics for all (not just skewed)")
parser.add_argument("--behave_group", action="store_true", default=False,help="Plot cohorts for behavioral groups")
parser.add_argument("--fontfamily", type=str, help="The font to use for plots", default='Brandon Grotesque')
parser.add_argument("--fontsize", type=int, help="The font to use for plots", default=20)



def plot_one_cohort_churn(cc,args,var_to_plot,plot_score):

    print('Plotting churn vs %s' % var_to_plot)
    renames = cc.get_conf('renames')
    if var_to_plot not in renames:
        renames[var_to_plot] = var_to_plot

    plot_frame = cc.behavioral_cohort_plot_data(var_to_plot, nbin=args.nbin)
    bins_used = plot_frame.shape[0]
    bins_zero = args.nbin - bins_used
    ax_scale=cc.get_conf('ax_scale')
    churn_plot_max = ceil(plot_frame['churn_rate'].max() * ax_scale) / 100.0

    if args.behave_group or not plot_score:
        plt.figure(figsize=(6, 4))
        plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                 marker='o', color='red', linewidth=2, label=var_to_plot)
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.xlabel('Cohort Average of  "%s"' % renames[var_to_plot])
        # plt.title('Churn vs. Cohorts of %s' % var_to_plot)
        plt.ylim(0, churn_plot_max)
        if args.hide_ax:
            plt.gca().get_yaxis().set_ticks(
                [0.25 * churn_plot_max, 0.5 * churn_plot_max, 0.75 * churn_plot_max, 1.0 * churn_plot_max])
            plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
            plt.ylabel('Cohort Churn (Relative)')
        else:
            plt.ylabel('Cohort Churn Rate (%)')
        plt.grid()

    else:
        score_frame = cc.behavioral_cohort_plot_data(var_to_plot,use_score=True, nbin=args.nbin)
        plt.figure(figsize=(10, 10))
        plt.subplot(2, 1, 1)
        plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                 marker='o', color='red', linewidth=2, label=var_to_plot)
        plt.ylabel('Cohort Churn Rate (%)')
        plt.xlabel('Cohort Average of  "%s"' % renames[var_to_plot])
        plt.grid()
        # plt.title('Churn vs. Cohorts of %s' % var_to_plot)
        plt.ylim(0, churn_plot_max)
        if args.hide_ax:
            plt.gca().get_yaxis().set_ticks(
                [0.25 * churn_plot_max, 0.5 * churn_plot_max, 0.75 * churn_plot_max, 1.0 * churn_plot_max])
            plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
            plt.ylabel('Cohort Churn (Relative)')
        else:
            plt.ylabel('Cohort Churn Rate (%)')

        plt.subplot(2, 1, 2)
        plt.plot(var_to_plot, 'churn_rate', data=score_frame,
                 marker='o', color='blue', linewidth=2, label='score(%s)' % var_to_plot)
        plt.xlabel('Cohort Average of  "%s" (SCORE)' % renames[var_to_plot])
        plt.grid()
        plt.ylim(0, churn_plot_max)
        if args.hide_ax:
            plt.gca().get_yaxis().set_ticks(
                [0.25 * churn_plot_max, 0.5 * churn_plot_max, 0.75 * churn_plot_max, 1.0 * churn_plot_max])
            plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
            plt.ylabel('Cohort Churn (Relative)')
        else:
            plt.ylabel('Cohort Churn Rate (%)')

    save_name = 'churn_vs_' + var_to_plot
    if args.hide_ax:
        save_name+='noax.png'

    plt.savefig(cc.save_path(save_name, ext='png'))
    plt.close()


def plot_dataset_cohorts(cc,args):

    plot_columns = cc.churn_metric_columns()
    data_scores, skewed_columns = cc.normalize_skewscale()

    if args.always_score:
        skewed_columns={c:True for c in plot_columns }

    if args.behave_group:
        cc.group_behaviors()
        plot_columns = cc.grouped_columns
        the_one_plot=None
        skewed_columns={c:False for c in plot_columns }
    else:
        plot_columns = cc.metric_columns
        the_one_plot=[l.lower() for l in args.metrics] if args.metrics is not None else None


    for var_to_plot in plot_columns:
        if the_one_plot is not None and var_to_plot not in the_one_plot: continue
        plot_one_cohort_churn(cc,args,var_to_plot,skewed_columns[var_to_plot])



if __name__ == "__main__":

    args, _ = parser.parse_known_args()

    font = {'family': args.fontfamily, 'size': args.fontsize}
    matplotlib.rc('font', **font)

    churn_calc = ChurnCalculator(args.schema)
    plot_dataset_cohorts(churn_calc,args)

