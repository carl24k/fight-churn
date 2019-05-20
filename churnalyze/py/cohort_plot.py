import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from math import ceil
import churn_calc as cc
from churn_const import save_path, schema_data_dict, load_mat_file, renames, skip_metrics,key_cols, no_plot, ax_scale

run_mets = None
behave_group = False
hideAx=False
allScores=False

font = {'family': 'Brandon Grotesque', 'size': 20}
matplotlib.rc('font', **font)

# schema = 'b'
# schema = 'v'
# schema = 'k'
schema = 'churnsim2'

# run_mets=['Detractor_Rate']
# run_mets=['klips_per_tab','data_sources_per_tab','time_per_edit','dashboard_views_per_day','edits_per_view']
# run_mets=['mrr']
# run_mets=['account_tenure']
# run_mets=['mrr','Use_Per_Base_Unit','Use_Per_Dollar_MRR','Percent_Canada','Percent_US','Percent_Intl','Percent_TollFree','Dollar_MRR_Per_Call_Unit','Dollar_MRR_Per_Base_Unit','Base_Units_per_Dollar_MRR_Per']
# run_mets=['account_tenure','Active_Users_Last_Qtr']
# run_mets=['active_users_per_seat','active_users_per_dollar_mrr','dollars_per_dashboard','dashboards_per_dollar_mrr','dash_views_per_user_per_month']
# run_mets=['active_users_per_dollar_mrr']
# run_mets=['Customer_added_Per_Dollar','CustomerPromoter_Per_Dollar','Contact_Per_Dollar','Transactions_Per_Dollar','Message_Viewed_Per_Dollar']

# For data council deck
# run_mets= ['Account_Active_Today_PerMonth'] # k
# run_mets=['ReviewUpdated_PerMonth','CustomerAdded_PerMonth'] # b
# run_mets=['ReviewUpdated_PerMonth'] # b
# run_mets=['Cost_Local_PerMonth', 'mrr'] # v
# run_mets=['Cost_Local_PerMonth','base_units','Cost_LD_Canada_PerMonth'] # v
# run_mets = ['CustomerPromoter_PerMonth','CustomerDetractor_PerMonth','Detractor_Rate']
# run_mets = ['num_seats','num_users','mrr','active_users_per_seat','active_users_per_dollar_mrr','dollars_per_active_user','Active_Users_Last_Qtr']
# run_mets = ['active_users_per_dollar_mrr']
# run_mets=['Detractor_Rate','Promoter_Rate']
# run_mets=['num_users','Active_Users_Last_Qtr','User_Utilization','num_seats']
# run_mets=['transactionadded_permonth']
# run_mets = ['orientation_switch_permonth']

data_file = schema_data_dict[schema]
schema_save_path = save_path(schema)+data_file
nbin=5

def main():
    churn_data = cc.data_load(schema)
    plot_columns = cc.churn_metric_columns(churn_data.columns.values)

    summary = cc.dataset_stats(churn_data,plot_columns)
    data_scores, skewed_columns = cc.normalize_skewscale(churn_data, plot_columns, summary)
    if allScores:
        skewed_columns={c:True for c in plot_columns }

    if behave_group:
        load_mat_df = pd.read_csv(save_path(schema, load_mat_file),index_col=0)
        num_weights = load_mat_df.astype(bool).sum(axis=0)
        load_mat_df = load_mat_df.loc[:,num_weights>1]
        grouped_columns=['Metric Group %d' % (d+1) for d in range(0,load_mat_df.shape[1])]
        churn_data_reduced = pd.DataFrame(np.matmul(data_scores[plot_columns].to_numpy(), load_mat_df.to_numpy()),columns=grouped_columns)
        churn_data_reduced['is_churn']=churn_data['is_churn']
        churn_data = churn_data_reduced
        plot_columns = grouped_columns
        the_one_plot=None
        skewed_columns={c:False for c in plot_columns }
    else:
        the_one_plot=[l.lower() for l in run_mets] if run_mets is not None else None


    for var_to_plot in plot_columns:
        if the_one_plot is not None and var_to_plot not in the_one_plot: continue

        print('Plotting churn vs %s' % var_to_plot)
        if var_to_plot not in renames:
            renames[var_to_plot]=var_to_plot

        plot_frame=cc.behavioral_cohort_plot_data(churn_data,var_to_plot,nbin=nbin)
        bins_used=plot_frame.shape[0]
        bins_zero=nbin-bins_used
        churn_plot_max = ceil(plot_frame['churn_rate'].max()* ax_scale[schema])/100.0

        if behave_group or not skewed_columns[var_to_plot]:
            plt.figure(figsize=(6,4))
            plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                     marker='o', color='red', linewidth=2, label=var_to_plot)
            plt.gcf().subplots_adjust(bottom=0.2)
            plt.xlabel('Cohort Average of  "%s"' % renames[var_to_plot])
            # plt.title('Churn vs. Cohorts of %s' % var_to_plot)
            plt.ylim(0, churn_plot_max)
            if hideAx:
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
            if hideAx:
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
            if hideAx:
                plt.gca().get_yaxis().set_ticks([ 0.25*churn_plot_max, 0.5*churn_plot_max, 0.75*churn_plot_max, 1.0*churn_plot_max])
                plt.gca().get_yaxis().set_ticklabels([])  # Hiding y axis labels on the count
                plt.ylabel('Cohort Churn (Relative)')
            else:
                plt.ylabel('Cohort Churn Rate (%)')

        if hideAx:
            saveName = schema_save_path + 'churn_vs_' + var_to_plot + '_noax.png'
        else:
            saveName = schema_save_path + 'churn_vs_' + var_to_plot + '.png'

        plt.savefig(saveName)
        plt.close()


if __name__ == "__main__":
    main()
