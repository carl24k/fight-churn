from fightchurn.run_churn_listing import sql_listing
from fightchurn.listings.chap3.listing_3_7_metric_qa_plot import metric_qa_plot

metric_qa_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_metric_stats_over_time'

run_total = False
run_distinct = False
run_freebies = False
run_highlights = False
run_read_ratio = True
run_downloads_per = False
run_total_time = False
rerun_reading = False
run_qa = False

if rerun_reading:
    param_dict = {
        '%new_metric_id': 17,
        '%event2measure': f'ReadingOwnedBook',
        '%new_metric_name': f'reading_book3'
    }

    sql_listing(3, 3, 'count_metric_insert', 'liveproject', 'run', param_dict)
    sql_listing(3, 4, 'metric_name_insert', 'liveproject', 'run', param_dict)
    metric_name = param_dict['%new_metric_name']
    param_dict['%metric2measure'] = metric_name
    sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=metric_name)


if run_total:
    param_dict = {
        '%new_metric_id': 20,
        '%new_metric_name': f'total_event_count12wk'
    }

    sql_listing(3, 17, 'total_metric_insert', 'liveproject', 'run', param_dict)
    sql_listing(3, 4, 'metric_name_insert', 'liveproject', 'run', param_dict)
    metric_name = param_dict['%new_metric_name']
    param_dict['%metric2measure'] = metric_name
    sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=metric_name)

if run_distinct:
    param_dict = {
        '%new_metric_id': 21,
        '%new_metric_name': f'distinct_product_count12wk'
    }
    sql_listing(3, 18, 'distinct_metric_insert', 'liveproject', 'run', param_dict)
    sql_listing(3, 4, 'metric_name_insert', 'liveproject', 'run', param_dict)
    param_dict['%metric2measure'] = param_dict['%new_metric_name']
    sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=param_dict['%new_metric_name'])

if run_freebies:
    param_dict = {
        '%from_yyyy-mm-dd': '2020-02-22',
        '%to_yyyy-mm-dd': '2020-06-01',
        '%new_metric_id': 23,
        '%new_metric_name': f'total_freebies_count12wk',
        '%metric_list': "'ReadingFreePreview_count12wk','FreeContentCheckout_count12wk','ReadingOpenChapter_count12wk'"
    }
    sql_listing(7, 3, 'total_metric', 'liveproject', 'run', param_dict,insert=True)
    param_dict['%metric2measure'] = param_dict['%new_metric_name']
    sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=param_dict['%new_metric_name'])
    metric_qa_plot(metric_qa_path, param_dict['%new_metric_name'])



if run_highlights:
    param_dict = {
        '%from_yyyy-mm-dd': '2020-02-22',
        '%to_yyyy-mm-dd': '2020-06-01',
        '%new_metric_id': 23,
        '%new_metric_name': f'total_highlights_count12wk',
        '%metric_list' : "'HighlightCreated_count12wk','CrossReferenceTermOpened_count12wk'"
    }
    sql_listing(7, 3, 'total_metric', 'liveproject', 'run', param_dict,insert=True)
    param_dict['%metric2measure'] = param_dict['%new_metric_name']
    sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=param_dict['%new_metric_name'])
    metric_qa_plot(metric_qa_path, param_dict['%new_metric_name'])




if run_read_ratio:
    param_dict = {
        '%from_yyyy-mm-dd': '2020-02-22',
        '%to_yyyy-mm-dd': '2020-06-01',
        '%new_metric_id': 28,
        '%new_metric_name': f'percent_reading_recalc',
        '%num_metric' : 'reading_book_recalc',
        '%den_metric' : 'total_event_count12wk'
    }
    sql_listing(7, 1, 'ratio_metric', 'liveproject', 'run', param_dict,insert=True)
    param_dict['%metric2measure'] = param_dict['%new_metric_name']
    sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=param_dict['%new_metric_name'])
    metric_qa_plot(metric_qa_path, param_dict['%new_metric_name'])



if run_downloads_per:
    param_dict = {
        '%from_yyyy-mm-dd': '2020-02-22',
        '%to_yyyy-mm-dd': '2020-06-01',
        '%new_metric_id': 25,
        '%new_metric_name': f'download_per_book',
        '%num_metric' : 'EBookDownloaded_count12wk',
        '%den_metric' : 'distinct_product_count12wk'
    }
    sql_listing(7, 1, 'ratio_metric', 'liveproject', 'run', param_dict,insert=True)
    param_dict['%metric2measure'] = param_dict['%new_metric_name']
    sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=param_dict['%new_metric_name'])
    metric_qa_plot(metric_qa_path, param_dict['%new_metric_name'])


if run_total_time:
    param_dict = {
        '%from_yyyy-mm-dd': '2020-02-22',
        '%to_yyyy-mm-dd': '2020-06-01',
        '%new_metric_id': 26,
        '%new_metric_name': f'total_time_reading'
    }
    sql_listing(3, 19, 'total_time_insert', 'liveproject', 'run', param_dict)
    sql_listing(3, 4, 'metric_name_insert', 'liveproject', 'run', param_dict)
    param_dict['%metric2measure'] = param_dict['%new_metric_name']





if run_qa:
    new_metrics = ['distinct_product_count12wk',
                   'total_highlights_count12wk', 'percent_reading', 'download_per_book',
                   'percent_reading', 'total_time_reading','total_freebies_count12k']

    new_metrics = [ 'total_freebies_count12k']

    param_dict = {
        '%from_yyyy-mm-dd': '2020-02-22',
        '%to_yyyy-mm-dd': '2020-06-01',
        '%new_metric_name': ''
    }

    for one_metric in new_metrics:
        param_dict['%metric2measure'] = one_metric
        sql_listing(3, 6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=one_metric)
        metric_qa_plot(metric_qa_path, one_metric)

    sql_listing(3, 8, 'metric_coverage', 'liveproject', 'save', {}, save_ext='qa_coverage')
