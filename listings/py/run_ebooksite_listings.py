import json

from run_churn_listing import sql_listing, python_listing
from listing_5_2_dataset_stats import  dataset_stats
from listing_5_1_cohort_plot import cohort_plot
from listing_5_5_cohort_plot_fixed import cohort_plot_fixed
from listing_6_1_metric_pair_plot import metric_pair_plot
from listing_6_2_dataset_correlation_matrix import dataset_correlation_matrix
from listing_5_3_metric_scores import metric_scores
from listing_6_4_find_metric_groups import find_metric_groups
from listing_6_3_apply_metric_groups import apply_metric_groups
from listing_6_5_ordered_correlation_matrix import ordered_correlation_matrix
from listing_8_2_logistic_regression import logistic_regression
from listing_9_4_regression_cparam import regression_cparam
from listing_9_5_crossvalidate import crossvalidate
from listing_9_2_top_decile_lift import top_decile_lift

datapath ='/Users/carl/Documents/churn/fight-churn-output/ebooksite/ebooksite_dataset.csv'
score_path = '/Users/carl/Documents/churn/fight-churn-output/ebooksite/ebooksite_dataset_scores.csv'
group_path = '/Users/carl/Documents/churn/fight-churn-output/ebooksite/ebooksite_dataset_groupscore.csv'

params = {
    "%from_yyyy-mm-dd": "2019-12-01",
    "%to_yyyy-mm-dd": "2020-06-01"
}

py_params = {
}

events = ['ReadingOwnedBook',
            'EBookDownloaded',
            'ReadingFreePreview',
            'HighlightCreated',
            'FreeContentCheckout',
            'ReadingOpenChapter',
            'WishlistItemAdded',
            'CrossReferenceTermOpened']

metrics_orig = ['numberbooksread_90d',
            'crossreferencetermopened_90d',
            'totalevents_90d',
            'highlightcreated_90d',
            'readingownedbook_90d',
            'ebookdownloaded_90d',
            'freecontentcheckout_90d',
            'readingopenchapter_90d',
            'readingfreepreview_90d']

metrics = ['ebookdownloaded_90d','numberbooksread_90d',
           'dayssincelastevent','downloads_per_book',
           'percent_reading_own_book','reading_feature_ratio',
           'readingownedbook_90d','totalevents_90d']

metrics_grouped=['metric_group_1','dayssincelastevent',
                 'downloads_per_book','percent_reading_own_book',
                 'reading_feature_ratio','readingownedbook_90d',
                 'totalevents_90d']

cparams = [0.008,0.004, 0.002, 0.001, 0.0005,0.00025]

def event_qa():
    sql_listing(3, 11, 'events_per_account', 'ebooksite', mode='save', param_dict=params)
    for e in events:
        params['%event2measure']=e
        sql_listing(3, 9, 'events_per_day', 'ebooksite', mode='save', param_dict=params, save_ext=e)
        py_params["event_name"]=e
        py_params["qa_data_path"]="../../../fight-churn-output/ebooksite/ebooksite_events_per_day"
        python_listing(3,10,'event_count_plot',param_dict=py_params)


def metric_calc():

    params['%new_metric_id'] = 9
    params["%new_metric_name"] = 'num_books_read_90d'
    sql_listing(3, 18, 'distinct_product_metric', 'ebooksite', mode='run', param_dict=params)
    sql_listing(3,4,'metric_name_insert','ebooksite',mode='run',param_dict=params)

    params['%new_metric_id'] = 8
    params["%new_metric_name"] = 'total_events_90d'
    sql_listing(3, 17, 'all_event_count_metric_insert', 'ebooksite', mode='run', param_dict=params)
    sql_listing(3,4,'metric_name_insert','ebooksite',mode='run',param_dict=params)

    for idx,e in enumerate(events):
        params['%event2measure']=e
        params['%new_metric_id']=idx
        sql_listing(3, 3, 'count_metric_insert', 'ebooksite', mode='run', param_dict=params)
        params["%new_metric_name"]=f'{e}_90d'
        sql_listing(3,4,'metric_name_insert','ebooksite',mode='run',param_dict=params)

def advanced_metric_calc():

    params['%new_metric_id'] = 27
    params['%new_metric_name'] = 'reading_features_90d'
    params['%metric_list'] = "'CrossReferenceTermOpened_90d_tenscale','ReadingFreePreview_90d_tenscale',  'HighlightCreated_90d_tenscale','FreeContentCheckout_90d_tenscale', 'ReadingOpenChapter_90d_tenscale','WishlistItemAdded_90d_tenscale'"
    sql_listing(7, 3, 'total_metric', 'ebooksite', mode='run', param_dict=params, insert=True)


    # params['%new_metric_id'] = 23
    # sql_listing(7, 12, 'days_since_any_event', 'ebooksite', mode='run', param_dict=params, insert=True)

def scaled_metrics():
    params['%obs_period'] = 90
    params['%desc_period'] = 90
    params['%min_tenure'] = 15
    params['%new_metric_id'] = 28
    params['%new_metric_name'] = 'numbooks_read_90d_tenscale'
    sql_listing(7, 13, 'tenure_scaled_books_read', 'ebooksite', mode='run', param_dict=params, insert=True)


    # params['%new_metric_id']=22
    # sql_listing(7, 11, 'ebook_scaled_total_events_per_month', 'ebooksite', mode='run', param_dict=params,insert=True)
    # params["%new_metric_name"] = f'total_events_90d_tenscale'
    # sql_listing(3, 4, 'metric_name_insert', 'ebooksite', mode='run', param_dict=params)

    # for idx,e in enumerate(events):
    #     params['%event2measure']=e
    #     params['%new_metric_id']=idx+14
    #     sql_listing(7, 10, 'ebook_scaled_events_per_month', 'ebooksite', mode='run', param_dict=params,insert=True)
    #     params["%new_metric_name"]=f'{e}_90d_tenscale'
    #     sql_listing(3,4,'metric_name_insert','ebooksite',mode='run',param_dict=params)


def tenure_metric():
    params['%new_metric_id'] = 13
    params["%new_metric_name"] = 'account_tenure'
    sql_listing(3,4,'metric_name_insert','ebooksite',mode='run',param_dict=params)
    sql_listing(3, 19, 'ebook_tenure_insert', 'ebooksite', mode='run', param_dict=params)


def metric_qa():
    sql_listing(3,8,'metric_coverage','ebooksite',mode='save',param_dict=params)

    # for e in events:
    #     m = f'{e}_90d'
    #     params["%metric2measure"]=m
    #     sql_listing(3,6,'metric_stats_over_time','ebooksite',mode='save',param_dict=params,save_ext=m)
    #     py_params["metric_name"] = m
    #     py_params["qa_data_path"]  = "../../../fight-churn-output/ebooksite/ebooksite_metric_stats_over_time"
    #     python_listing(3, 7, 'metric_qa_plot', param_dict=py_params)



def observations():
    sql_listing(4,7,'ebooksite_observations','ebooksite',mode='run',param_dict=params)


def dataset():
    params['%metric_interval']=7
    sql_listing(4,8,'dataset','ebooksite',mode='save',param_dict=params)


def dataset_qa():
    dataset_stats(datapath)


def cohort_plots():
    cohort_plot(datapath, 'downloads_per_book',ncohort=3)
    # cohort_plot_fixed(datapath,'downloads_per_book',cuts=(-1e6,0.01,1.0,1e6))

    # for m in metrics:
    #     cohort_plot(datapath,m)
    # cohort_plot(datapath, 'total_reading_features_90d')
    # cohort_plot(datapath, 'percent_reading_own_book')
    # cohort_plot(datapath, 'dayssincelastevent')
    # # These two work better with fixed cuts
    # cohort_plot_fixed(datapath,'crossreferencetermopened_90d',cuts=(-1e6,0.01,1e6))
    # cohort_plot_fixed(datapath,'highlightcreated_90d',cuts=(-1e6,0.01,1e6))


def standard_correlation():
    dataset_correlation_matrix(datapath)
    for m in range(len(metrics)):
        for n in range(m):
            if m==n:
                continue
            m1=metrics[m]
            m2=metrics[n]
            print(f'Ploting {m1} vs {m2}')
            metric_pair_plot(datapath,m1,m2)



def scores_correlation():
    dataset_correlation_matrix(score_path)
    # for m in range(len(metrics)):
    #     for n in range(m):
    #         if m==n:
    #             continue
    #         m1=metrics[m]
    #         m2=metrics[n]
    #         print(f'Ploting {m1} vs {m2}')
    #         metric_pair_plot(score_path,m1,m2)


def score_dataset():
    metric_scores(data_set_path=datapath,skew_thresh=12)
    dataset_stats(score_path)


def average_scores():
    find_metric_groups(datapath, group_corr_thresh=0.63)
    apply_metric_groups(datapath)
    ordered_correlation_matrix(datapath)
    dataset_correlation_matrix(group_path)


def group_cohorts():
    # cohort_plot(group_path, 'metric_group_1')
    # cohort_plot(group_path, 'metric_group_2')
    for m in metrics_grouped:
        cohort_plot(group_path,m)

def ratio_metrics_v1():
    params['%num_metric']='EBookDownloaded_90d'
    params['%den_metric']='num_books_read_90d'
    params['%new_metric_name'] = 'downloads_per_book_90d'
    params['%new_metric_id'] = 11
    sql_listing(7,1,'ratio_metric','ebooksite',mode='run',param_dict=params,insert=True)

    params['%num_metric']='total_events_90d'
    params['%den_metric']='num_books_read_90d'
    params['%new_metric_name'] = 'events_per_book_90d'
    params['%new_metric_id'] = 12
    sql_listing(7,1,'ratio_metric','ebooksite',mode='run',param_dict=params,insert=True)

    # params['%num_metric']='ReadingOwnedBook_90d'
    # params['%den_metric']='num_books_read_90d'
    # params['%new_metric_name'] = 'reads_per_book_90d'
    # params['%new_metric_id'] = 10
    # sql_listing(7,1,'ratio_metric','ebooksite',mode='run',param_dict=params,insert=True)


def ratio_cohorts():
    cohort_plot(datapath,'reading_feature_ratio')
    cohort_plot(datapath,'percent_reading_features')
    # cohort_plot(datapath,'reads_per_book_90d')
    # cohort_plot(datapath,'downloads_per_book_90d')
    # cohort_plot(datapath,'events_per_book_90d')


def ratio_metrics_v2():
    params['%num_metric']='reading_features_90d'
    params['%den_metric']='ReadingOwnedBook_90d_tenscale'
    params['%new_metric_name'] = 'reading_feature_book_ratio'
    params['%new_metric_id'] = 31
    sql_listing(7,1,'ratio_metric', 'ebooksite',mode='run',param_dict=params,insert=True)

    # params['%num_metric']='reading_features_90d'
    # params['%den_metric']='total_events_90d_tenscale'
    # params['%new_metric_name'] = 'percent_reading_features'
    # params['%new_metric_id'] = 30
    # sql_listing(7,1,'ratio_metric', 'ebooksite',mode='run',param_dict=params,insert=True)

    # params['%num_metric']='EBookDownloaded_90d_tenscale'
    # params['%den_metric']='numbooks_read_90d_tenscale'
    # params['%new_metric_name'] = 'downloads_per_book_tenscale'
    # params['%new_metric_id'] = 29
    # sql_listing(7,1,'ratio_metric', 'ebooksite',mode='run',param_dict=params,insert=True)

    # params['%num_metric']='EBookDownloaded_90d_tenscale'
    # params['%den_metric']='num_books_read_90d'
    # params['%new_metric_name'] = 'percent_events_download'
    # params['%new_metric_id'] = 25
    # sql_listing(7,1,'ratio_metric', 'ebooksite',mode='run',param_dict=params,insert=True)

    # params['%num_metric']='ReadingOwnedBook_90d_tenscale'
    # params['%den_metric']='total_events_90d_tenscale'
    # params['%new_metric_name'] = 'percent_events_readingown'
    # params['%new_metric_id'] = 24
    # sql_listing(7,1,'ratio_metric', 'ebooksite',mode='run',param_dict=params,insert=True)


def simple_regression():
    logistic_regression(datapath)


def regression_control_params():

    for c in cparams:
        regression_cparam(datapath,c)


def regression_crossvalidate():
    crossvalidate(datapath,3,cparams)


def lift_demo():
    top_decile_lift(datapath,predict_retention=True)


if __name__ == "__main__":

    function_map = {
        '1' : 'event_qa',
        '2': 'metric_calc',
        '3': 'metric_qa',
        '4' : 'observations',
        '5' : 'dataset',
        '6' : 'dataset_qa',
        '7' : 'cohort_plots',
        '8' : 'standard_correlation',
        '9' : 'score_dataset',
        'A' : 'scores_correlation',
        'B' : 'average_scores',
        'C' : 'group_cohorts',
        'D' : 'ratio_metrics',
        'E' : 'ratio_cohorts',
        'F' : 'tenure_metric',
        'G' : 'scaled_metrics',
        'H' : 'advanced_metric_calc',
        'I' : 'ratio_metrics_v2',
        'J' : 'simple_regression',
        'K' : 'regression_control_params',
        'L' : 'regression_crossvalidate',
        'M' : 'lift_demo'
}

    print(json.dumps(function_map,indent=4))
    to_run = input('Enter steps to run: ')
    for c in to_run.split(sep=' '):
        if c.upper() in function_map:
            print(f'Running {function_map[c.upper()]}')
            locals()[function_map[c.upper()]]()
        else:
            print('******************************')
            print(f'* NO FUNCTION FOR INPUT "{c}" !')
            print('******************************')