
from run_churn_listing import sql_listing, python_listing


params = {
    "%from_yyyy-mm-dd": "2019-12-01",
    "%to_yyyy-mm-dd": "2020-06-01"
}

py_params = {
    "event_name": "like"
}

# sql_listing(3,11,'events_per_account','livebook',mode='save',param_dict=params)

events = ['ReadingOwnedBook',
    'FirstLivebookAccess',
    'FirstManningAccess',
    'EBookDownloaded',
    'ReadingFreePreview',
    'HighlightCreated',
    'FreeContentCheckout',
    'ReadingOpenChapter'
]

if False:
    for e in events:
        params['%event2measure']=e
        sql_listing(3, 9, 'events_per_day', 'livebook', mode='save', param_dict=params, save_ext=e)
        py_params["event_name"]=e
        py_params["qa_data_path"]="../../../fight-churn-output/livebook/livebook_events_per_day",
        python_listing(3,10,'event_count_plot',param_dict=py_params)


if False:
    for idx,e in enumerate(events):
        params['%event2measure']=e
        params['%new_metric_id']=idx
        sql_listing(3, 3, 'count_metric_insert', 'livebook', mode='run', param_dict=params)
        params["%new_metric_name"]=f'{e}_90d'
        sql_listing(3,4,'metric_name_insert','livebook',mode='run',param_dict=params)

if False:
    for e in events:
        m = f'{e}_90d'
        params["%metric2measure"]=m
        sql_listing(3,6,'metric_stats_over_time','livebook',mode='save',param_dict=params,save_ext=m)
        py_params["metric_name"] = m
        py_params["qa_data_path"]  = "../../../fight-churn-output/livebook/livebook_metric_stats_over_time"
        python_listing(3, 7, 'metric_qa_plot', param_dict=py_params)

sql_listing(3,8,'metric_coverage','livebook',mode='save',param_dict=params)