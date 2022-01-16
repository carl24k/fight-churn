from fightchurn.run_churn_listing import sql_listing
from fightchurn.listings.chap3.listing_3_7_metric_qa_plot import metric_qa_plot


all_events = ['ReadingOwnedBook', 'FirstLivebookAccess', 'FirstManningAccess', 'EBookDownloaded',
              'ReadingFreePreview', 'HighlightCreated', 'FreeContentCheckout', 'ReadingOpenChapter',
              'ProductTocLivebookLinkOpened', 'LivebookLogin', 'DashboardLivebookLinkOpened',
              'WishlistItemAdded', 'CrossReferenceTermOpened', 'SearchMade']

metric_events = ['ReadingOwnedBook','EBookDownloaded','ReadingFreePreview','HighlightCreated','FreeContentCheckout','ReadingOpenChapter','ProductTocLivebookLinkOpened','LivebookLogin','DashboardLivebookLinkOpened','WishlistItemAdded','CrossReferenceTermOpened','SearchMade','SearchResultOpened','ProductLookInsideLivebookLinkOpened']


calc =  False
qa = True

if calc:
    for idx, event in enumerate(metric_events):
        param_dict = {
            '%from_yyyy-mm-dd': '2020-02-22',
            '%to_yyyy-mm-dd': '2020-06-01',
            '%new_metric_id' : idx,
            '%event2measure': event
        }
        sql_listing(3,3, 'count_metric_insert', 'liveproject', 'run', param_dict)
        param_dict = {
            '%new_metric_id' : idx,
            '%new_metric_name' : f'{event}_count12wk'
        }
        sql_listing(3,4, 'metric_name_insert', 'liveproject', 'run', param_dict)


metric_qa_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_metric_stats_over_time'


if qa:
    for idx, event in enumerate(metric_events):
        metric_name = f'{event}_count12wk'
        param_dict = {
            '%from_yyyy-mm-dd': '2020-02-22',
            '%to_yyyy-mm-dd': '2020-06-01',
            '%metric2measure':  metric_name
        }
        sql_listing(3,6, 'metric_stats_over_time', 'liveproject', 'save', param_dict, save_ext=metric_name)
        metric_qa_plot(metric_qa_path, metric_name)
