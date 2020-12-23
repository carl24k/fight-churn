from run_churn_listing import sql_listing
from listing_3_7_metric_qa_plot import metric_qa_plot
from listing_3_10_event_count_plot import event_count_plot

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

sql_params = {
    "%from_yyyy-mm-dd": "2019-12-01",
    "%to_yyyy-mm-dd": "2020-06-01"
}

schema='livebook'


def event_qa():
    sql_listing(3, 11, 'events_per_account', schema, mode='save', param_dict=sql_params)
    for e in events:
        sql_params['%event2measure']=e
        sql_listing(3, 9, 'events_per_day', schema, mode='save', param_dict=sql_params, save_ext=e)
        event_count_plot("../../../fight-churn-output/livebook/livebook_events_per_day",e)


def metric_calc():

    for idx,e in enumerate(events):
        sql_params['%event2measure']=e
        sql_params['%new_metric_id']=idx
        sql_listing(3, 3, 'count_metric_insert', schema, mode='run', param_dict=sql_params)
        sql_params["%new_metric_name"]= f'{e}_90d'
        sql_listing(3, 4,'metric_name_insert', schema, mode='run', param_dict=sql_params)


def metric_qa():
    sql_listing(3, 8,'metric_coverage', schema, mode='save', param_dict=sql_params)
    for e in events:
        m = f'{e}_90d'
        sql_params["%metric2measure"]=m
        sql_listing(3, 6,'metric_stats_over_time', schema, mode='save', param_dict=sql_params, save_ext=m)
        metric_qa_plot("../../../fight-churn-output/livebook/livebook_metric_stats_over_time", m)


if __name__ == "__main__":
    event_qa()
    # metric_calc()
    metric_qa()
