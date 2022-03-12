from fightchurn.run_churn_listing import sql_listing
from fightchurn.listings.chap5.listing_5_1_cohort_plot import cohort_plot


dataset_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_dataset.csv'


metrics = [
    'readingownedbook',
    'ebookdownloaded',
    'readingfreepreview',
    'freecontentcheckout',
    'readingopenchapter',
    'producttoclivebooklinkopened',
    'livebooklogin',
    'dashboardlivebooklinkopened',
    'searchmade',
    'searchresultopened',
    'productlookinsidelivebooklinkopened'
]

rare_metrics = [
    'wishlistitemadded',
    'crossreferencetermopened',
    'highlightcreated',

]

for met in rare_metrics:
    cohort_plot(dataset_path, met,2)

# for met in metrics:
#     cohort_plot(dataset_path, met)

