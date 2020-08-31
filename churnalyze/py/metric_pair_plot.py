import sys
import matplotlib.pyplot as plt
import matplotlib
import argparse
from itertools import permutations
import numpy as np

from churn_calc import ChurnCalculator

parser = argparse.ArgumentParser()
# Main run control arguments
parser.add_argument("--schema", type=str, help="The name of the schema", default='churnsim2')
parser.add_argument("--metrics", type=str,nargs=2, help="Two metrics to plot (if not plotting all pairs)")


# Additional options
parser.add_argument("--hideax", action="store_true", default=False,help="Hide axis labeling for publication of case studies")
parser.add_argument("--score", action="store_true", default=False,help="Plot Scores vs Scores")

# parser.add_argument("--fontfamily", type=str, help="The font to use for plots", default='Brandon Grotesque')
# parser.add_argument("--fontsize", type=int, help="The font to use for plots", default=14)

parser.add_argument("--ylim", type=float, nargs=2, help="The y maximum", default=None)
parser.add_argument("--xlim", type=float, nargs=2, help="The y maximum", default=None)


def plot_pair(cc,args,metric1,metric2):
    '''
    Uses matplotlib scatter to plot two metrics from a churn calculator data set.
    Command line arguments control the choice to plot the metric as scores versus the metric on
    the natural scale, as well as options to hide the axes and choose limits.

    Note that if the metrics are listed in the "renames" section of the JSON configuration then those names
    will be shown in the displayed labels.

    :param cc: A churn calculator object
    :param args: The command line arguments produced by argparse
    :param metric1: The first metric name (string)
    :param metric2: The second metric name (string)
    :return:
    '''

    renames = cc.get_renames()

    met1_label = metric1 if not metric1 in renames else renames[metric1]
    met2_label = metric2 if not metric2 in renames else renames[metric2]
    if not args.score:
        met1_data = cc.churn_data[metric1]
        met2_data = cc.churn_data[metric2]
        save_name = metric1 + '_vs_' + metric2
    else:
        scores,_ = cc.normalize_skewscale()
        met1_data = scores[metric1]
        met2_data = scores[metric2]
        met1_label='Score('+met1_label+')'
        met2_label='Score('+met2_label+')'
        save_name = metric1 + 'S_vs_' + metric2 + 'S'

    print('Plotting ' + save_name)
    corr = met1_data.corr(met2_data)

    plt.figure(figsize=(6, 6))
    downsamp = 10
    # https://stackoverflow.com/questions/1403674/pythonic-way-to-return-list-of-every-nth-item-in-a-larger-list
    if downsamp>1:
        plt.scatter(met1_data[0::downsamp],met2_data[0::downsamp], marker='.',color='black')
    else:
        plt.scatter(met1_data,met2_data, marker='.',color='black')

    plt.xlabel(met1_label)
    plt.ylabel(met2_label)
    plt.title('Correlation = %.2f' % corr)
    plt.tight_layout()
    if args.ylim is not None:
        plt.ylim(args.ylim[0],args.ylim[1])
    if args.xlim is not None:
        plt.xlim(args.xlim[0],args.xlim[1])

    if args.hideax and not args.score:
        plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
        plt.gca().get_xaxis().set_ticklabels([])  # Hiding y axis labels on the count
        save_name += '_noax'

    plt.grid()
    plt.savefig(cc.save_path(save_name, ext='svg',subdir='pair_scatter_plots'))
    plt.close()

if __name__ == "__main__":
    '''
    Uses parse args definitions at the top of this file. If no metrics are specified in the args then
    it will offer to plot all the pairs.
    '''

    args, _ = parser.parse_known_args()

    # font = {'family': args.fontfamily, 'size': args.fontsize}
    # matplotlib.rc('font', **font)

    churn_calc = ChurnCalculator(args.schema)

    if args.metrics is not None:
        plot_pair(churn_calc, args, args.metrics[0],args.metrics[1])
    else:
        all_mets = churn_calc.metric_columns
        nmet=len(all_mets)
        if input("Plot all pairs of %d metrics (%d plots) : are you sure? (enter %s to proceed) " %
                 (nmet,nmet*(nmet-1),args.schema)) != args.schema:
            exit(0)
        plot_pairs = permutations(all_mets,2)
        for pair in plot_pairs:
            plot_pair(churn_calc,args,pair[0],pair[1])
