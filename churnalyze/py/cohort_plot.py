import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import churn_calc as cc
from churn_const import save_path, schema_data_dict, load_mat_file

run_mets = None
behave_group = False

# schema = 'b'
# schema = 'v'
schema = 'k'

# run_mets=['Detractor_Rate']
# run_mets=['klips_per_tab','data_sources_per_tab','time_per_edit','dashboard_views_per_day','edits_per_view']
# run_mets=['mrr']
# run_mets=['account_tenure']
# run_mets=['Use_Per_Base_Unit','Use_Per_Dollar_MRR','Percent_Canada','Percent_US','Percent_Intl','Percent_TollFree','Dollar_MRR_Per_Call_Unit','Dollar_MRR_Per_Base_Unit']
# run_mets=['account_tenure','Active_Users_Last_Qtr']
# run_mets=['active_users_per_seat','active_users_per_dollar_mrr','dollars_per_dashboard','dashboards_per_dollar_mrr','dash_views_per_user_per_month']
# run_mets=['active_users_per_dollar_mrr']
# run_mets=['Customer_added_Per_Dollar','CustomerPromoter_Per_Dollar','Contact_Per_Dollar','Transactions_Per_Dollar','Message_Viewed_Per_Dollar']
run_mets= ['billing_period']

data_file = schema_data_dict[schema]
schema_save_path = save_path(schema)+data_file
nbin=8

def main():
    churn_data = pd.read_csv(schema_save_path+'.csv',index_col=0)
    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    plot_columns = cc.churn_metric_columns(churn_data.columns.values)

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
        the_one_plot=[l.lower() for l in run_mets] if run_mets is not None else None


    for var_to_plot in plot_columns:
        if the_one_plot is not None and var_to_plot not in the_one_plot: continue

        print('Plotting churn vs %s' % var_to_plot)

        plot_frame=cc.behavioral_cohort_plot_data(churn_data,var_to_plot,nbin=nbin)
        churn_plot_max = ceil(plot_frame['churn_rate'].max()*110.0)/100.0

        if behave_group or not skewed_columns[var_to_plot]:
            plt.figure(figsize=(4,6))
            plt.plot(var_to_plot, 'churn_rate', data=plot_frame,
                     marker='o', color='red', linewidth=2, label=var_to_plot)
            plt.title('Churn vs. Cohorts of %s' % var_to_plot)
            plt.legend()
            plt.ylabel('Cohort churn rate')
            plt.ylim(0, churn_plot_max)
        else:
            score_frame = cc.behavioral_cohort_plot_data(data_scores, var_to_plot,nbin=nbin)
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
