import json

from run_churn_listing import sql_listing, python_listing
from listing_5_2_dataset_stats import  dataset_stats
from listing_5_1_cohort_plot import cohort_plot
from listing_5_5_cohort_plot_fixed import cohort_plot_fixed
from listing_6_1_metric_pair_plot import metric_pair_plot
from listing_6_2_dataset_correlation_matrix import dataset_correlation_matrix
from listing_5_3_metric_scores import metric_scores

datapath ='/Users/carl/Documents/churn/fight-churn-output/ebooksite/ebooksite_dataset.csv'
score_path = '/Users/carl/Documents/churn/fight-churn-output/ebooksite/ebooksite_dataset_scores.csv'

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

metrics = ['numberbooksread_90d',
            'crossreferencetermopened_90d',
            'totalevents_90d',
            'highlightcreated_90d',
            'readingownedbook_90d',
            'ebookdownloaded_90d',
            'freecontentcheckout_90d',
            'readingopenchapter_90d',
            'readingfreepreview_90d']


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


def metric_qa():
    for e in events:
        m = f'{e}_90d'
        params["%metric2measure"]=m
        sql_listing(3,6,'metric_stats_over_time','ebooksite',mode='save',param_dict=params,save_ext=m)
        py_params["metric_name"] = m
        py_params["qa_data_path"]  = "../../../fight-churn-output/ebooksite/ebooksite_metric_stats_over_time"
        python_listing(3, 7, 'metric_qa_plot', param_dict=py_params)

    sql_listing(3,8,'metric_coverage','ebooksite',mode='save',param_dict=params)


def observations():
    sql_listing(4,7,'ebooksite_observations','ebooksite',mode='run',param_dict=params)


def dataset():
    params['%metric_interval']=7
    sql_listing(4,8,'dataset','ebooksite',mode='save',param_dict=params)


def dataset_qa():
    dataset_stats(datapath)


def cohort_plots():
    for m in metrics:
        cohort_plot(datapath,m)
    # These two work better with fixed cuts
    cohort_plot_fixed(datapath,'crossreferencetermopened_90d',cuts=(-1e6,0.01,1e6))
    cohort_plot_fixed(datapath,'highlightcreated_90d',cuts=(-1e6,0.01,1e6))


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


def score_dataset():
    metric_scores(data_set_path=datapath)
    dataset_stats(score_path)


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
        '9' : 'score_dataset'
    }

    print(json.dumps(function_map,indent=4))
    to_run = input('Enter steps to run:')
    for c in to_run.split(sep=' '):
        if c in function_map:
            print(f'Running {function_map[c]}')
            locals()[function_map[c]]()
        else:
            print('******************************')
            print(f'* NO FUNCTION FOR INPUT "{c}" !')
            print('******************************')