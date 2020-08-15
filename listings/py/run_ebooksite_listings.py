import click

from run_churn_listing import sql_listing, python_listing
from listing_5_2_dataset_stats import  dataset_stats
from listing_5_1_cohort_plot import cohort_plot

datapath='/Users/carl/Documents/churn/fight-churn-output/ebooksite/ebooksite_dataset.csv'

params = {
    "%from_yyyy-mm-dd": "2019-12-01",
    "%to_yyyy-mm-dd": "2020-06-01"
}

py_params = {
}

if click.confirm('Do you want to run Events per Account QA??', default=False):
    sql_listing(3, 11, 'events_per_account', 'ebooksite', mode='save', param_dict=params)

events = ['ReadingOwnedBook',
    'EBookDownloaded',
    'ReadingFreePreview',
    'HighlightCreated',
    'FreeContentCheckout',
    'ReadingOpenChapter',
    'WishlistItemAdded',
    'CrossReferenceTermOpened']


if click.confirm('Do you want to run Event v Time QA??', default=False):
    for e in events:
        params['%event2measure']=e
        sql_listing(3, 9, 'events_per_day', 'ebooksite', mode='save', param_dict=params, save_ext=e)
        py_params["event_name"]=e
        py_params["qa_data_path"]="../../../fight-churn-output/ebooksite/ebooksite_events_per_day"
        python_listing(3,10,'event_count_plot',param_dict=py_params)


if click.confirm('Do you want to run Metric Calculation??', default=False):
    for idx,e in enumerate(events):
        params['%event2measure']=e
        params['%new_metric_id']=idx
        sql_listing(3, 3, 'count_metric_insert', 'ebooksite', mode='run', param_dict=params)
        params["%new_metric_name"]=f'{e}_90d'
        sql_listing(3,4,'metric_name_insert','ebooksite',mode='run',param_dict=params)



if click.confirm('Do you want to run Metric QA??', default=False):
    for e in events:
        m = f'{e}_90d'
        params["%metric2measure"]=m
        sql_listing(3,6,'metric_stats_over_time','ebooksite',mode='save',param_dict=params,save_ext=m)
        py_params["metric_name"] = m
        py_params["qa_data_path"]  = "../../../fight-churn-output/ebooksite/ebooksite_metric_stats_over_time"
        python_listing(3, 7, 'metric_qa_plot', param_dict=py_params)

    sql_listing(3,8,'metric_coverage','ebooksite',mode='save',param_dict=params)


if click.confirm('Do you want to create observations??', default=False):
    sql_listing(4,7,'ebooksite_observations','ebooksite',mode='run',param_dict=params)


if click.confirm('Do you want to Create the Dataset??', default=False):
    params['%metric_interval']=7
    sql_listing(4,8,'dataset','ebooksite',mode='save',param_dict=params)


if click.confirm('Do you want to run Data Set Stats??', default=False):
    dataset_stats(datapath)

if click.confirm('Do you want to run Cohort Plots??', default=False):
    cohort_plot(datapath,'readingownedbook_90d')
    cohort_plot(datapath,'ebookdownloaded_90d')
    cohort_plot(datapath,'highlightcreated_90d')
    cohort_plot(datapath,'freecontentcheckout_90d')
    cohort_plot(datapath,'readingopenchapter_90d')
    cohort_plot(datapath,'readingfreepreview_90d')
    cohort_plot(datapath,'wishlistitemadded_90d')
    cohort_plot(datapath,'crossreferencetermopened_90d')
