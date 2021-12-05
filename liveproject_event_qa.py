from fightchurn.run_churn_listing import sql_listing
from fightchurn.listings.chap3.listing_3_10_event_count_plot import event_count_plot


event_qa_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_events_per_day'

all_events = ['ReadingOwnedBook', 'FirstLivebookAccess', 'FirstManningAccess', 'EBookDownloaded',
              'ReadingFreePreview', 'HighlightCreated', 'FreeContentCheckout', 'ReadingOpenChapter',
              'ProductTocLivebookLinkOpened', 'LivebookLogin', 'DashboardLivebookLinkOpened',
              'WishlistItemAdded', 'CrossReferenceTermOpened', 'SearchMade']

param_dict = {
    '%from_yyyy-mm-dd' : '2019-12-01',
    '%to_yyyy-mm-dd' : '2020-06-01',
    '%event2measure' : ''
}

for event in all_events:
    param_dict['%event2measure'] = event
    sql_listing(3,9, 'events_per_day', 'liveproject', 'save', param_dict,
                save_ext=param_dict['%event2measure'])

    event_count_plot(event_qa_path,param_dict['%event2measure'])
