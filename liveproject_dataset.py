from fightchurn.run_churn_listing import sql_listing
from fightchurn.listings.chap5.listing_5_2_dataset_stats import dataset_stats

 # Extracting the data
param_dict = {}
sql_listing(4, 6, 'current_customers', 'liveproject', 'save', param_dict, save_ext='')

dataset_path = '/Users/carl/Documents/churn/liveproject_stream_output/liveproject/liveproject_current_customers.csv'

dataset_stats(dataset_path)
