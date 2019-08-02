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
    '''
    Makes a plot of churn rates in behavioral cohorts for the dataset contained in the churn calculator.
    The function ChurnCalculator.behavioral_cohort_analysis actually calculates the cohorts, churn ratesa and
    average values and this function is concerned with presentation.

    Command line arguments control other features:
    1. Plot the grouped behavioral metrics or plain metrics,
    2. Always plot scored metrics, or the default of plotting scores only for skewed metrics
    3. Hide the axes scales (for use on case study data)
    4. Number of bins to suggest for cohorts (defaults to 10)

    There is also a plot scaling configuration in the schema_churnalyze.json - this will give a uniform maximum to
    all of the cohort plots, by scaling the churn rate. That way the different cohort plots are easier to compare.
    Usually scaling it to 2x the maximum churn rate is good, but this parameter allows adjustment. The parameter is
    given as an integer where 200 means set the maximum to 2x the churn rate, 300 means 3x the churn rate, etc.
    The code here also ensures that the chosen maximum is a whole number of percents (as a decimal) i.e. 0.10 or 0.11
     but not 0.1085 or some odd number of decimal places.

    :param cc: ChurnCalculator object created from schema given on the command line
    :param args: Command line arguments from argparse (defined at the top of this file)
    :param var_to_plot: string name of the metric to plot the cohorts of
    :param plot_score: boolean indicates scored version of metric should be plotted as well
    :return:
    '''

    print('Plotting churn vs %s' % var_to_plot)
    renames = cc.get_renames()
    if var_to_plot not in renames:
        renames[var_to_plot] = var_to_plot
    # First plot should always be the unscored version
    plot_frame = cc.behavioral_cohort_analysis(var_to_plot, nbin=args.nbin,use_score=False,use_group=args.behave_group)
    ax_scale=cc.get_conf('ax_scale',default=200)
    churn_plot_max = ceil(cc.churn_rate() * ax_scale) / 100.0

    if args.behave_group or not plot_score:
        plt.figure(figsize=(6, 4))
        plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                 marker='o', color='red', linewidth=2, label=var_to_plot)
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.xlabel('Cohort Average of  "%s"' % renames[var_to_plot])
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
        score_frame = cc.behavioral_cohort_analysis(var_to_plot, use_score=True, nbin=args.nbin)
        plt.figure(figsize=(10, 10))
        plt.subplot(2, 1, 1)
        plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                 marker='o', color='red', linewidth=2, label=var_to_plot)
        plt.ylabel('Cohort Churn Rate (%)')
        plt.xlabel('Cohort Average of  "%s"' % renames[var_to_plot])
        plt.grid()
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
        save_name+='noax'

    plt.savefig(cc.save_path(save_name, ext='png', subdir=cc.grouping_correlation_subdir(args.behave_group)))
    plt.close()


def plot_dataset_cohorts(cc,args):
    '''
    This function will run all columns, unless a list of metrics was supplied in the args in which case only those
    listed are plotted. Options to plot all cohorts with scored versions or to apply behavioral grouping are applied
    at the data set level, before looping over individual metrics and calling the plot_one_cohort_churn function.

    Note that column headers in the dataset are assumed to be all lower case so metric names are lower cased to make sure.
    :param cc: ChurnCalculator object created from schema given on the command line
    :param args: Command line arguments from argparse (defined at the top of this file)
    :return:
    '''

    plot_columns = cc.churn_metric_columns()
    data_scores, skewed_columns = cc.normalize_skewscale()

    if args.always_score:
        skewed_columns={c:True for c in plot_columns }

    if args.behave_group:
        cc.calc_behavior_groups()
        cc.apply_behavior_grouping()
        plot_columns = cc.grouped_columns
        list_to_plot=None
        skewed_columns={c:False for c in plot_columns }
    else:
        plot_columns = cc.metric_columns
        list_to_plot=[l.lower() for l in args.metrics] if args.metrics is not None else None


    for var_to_plot in plot_columns:
        if list_to_plot is not None and var_to_plot not in list_to_plot: continue
        plot_one_cohort_churn(cc,args,var_to_plot,skewed_columns[var_to_plot])



if __name__ == "__main__":

    # Uses parse args definitions at the top of this file.
    args, _ = parser.parse_known_args()

    font = {'family': args.fontfamily, 'size': args.fontsize}
    matplotlib.rc('font', **font)

    churn_calc = ChurnCalculator(args.schema)
    plot_dataset_cohorts(churn_calc,args)

