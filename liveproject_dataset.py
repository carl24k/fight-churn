from fightchurn.run_churn_listing import sql_listing
from fightchurn.listings.chap5.listing_5_2_dataset_stats import dataset_stats

# Extracting the data
current = False
past = True

if current:
    param_dict = {}
    sql_listing(4, 6, 'current_customers', 'liveproject', 'save', param_dict, save_ext='')

    dataset_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_current_customers.csv'

    # Run QA Stats
    dataset_stats(dataset_path)

if past:
    param_dict = {
        '%from_yyyy-mm-dd' : '2020-01-01',
        '%to_yyyy-mm-dd' : '2020-03-01',
        '%metric_interval' : '28 days'
    }
    sql_listing(4, 5, 'dataset', 'liveproject', 'save', param_dict, save_ext='')

    dataset_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_dataset.csv'

    # Run QA Stats
    dataset_stats(dataset_path)
