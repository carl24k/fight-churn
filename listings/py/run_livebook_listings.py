
from run_churn_listing import sql_listing, python_listing


params = {
    "%from_yyyy-mm-dd": "2019-12-01",
    "%to_yyyy-mm-dd": "2020-06-01"
}

py_params = {
    "qa_data_path": "../../../fight-churn-output/livebook/livebook_events_per_day",
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

for e in events:
    params['%event2measure']=e
    sql_listing(3, 9, 'events_per_day', 'livebook', mode='save', param_dict=params, save_ext=e)
    py_params["event_name"]=e
    python_listing(3,10,'event_count_plot',param_dict=py_params)
