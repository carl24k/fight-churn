from listing_5_1_cohort_plot import cohort_plot
from listing_5_2_dataset_stats import dataset_stats
from run_churn_listing import sql_listing

livebook_data_path = '../../../fight-churn-output/livebook/livebook_dataset.csv'

def observations():
    sql_listing(4, 7, 'create_observation', 'livebook', mode='save', param_dict={})
    sql_listing(4, 8, 'livebook_observations', 'livebook', mode='save', param_dict={})

def dataset():
    sql_listing(4, 9, 'dataset', 'livebook', mode='save', param_dict={})
    dataset_stats(livebook_data_path)

def cohorts():
    metrics = ['readingownedbook',
                'ebookdownloaded',
                'readingfreepreview',
                'highlightcreated',
                'freecontentcheckout',
                'readingopenchapter',
                'wishlistitemadded',
                'crossreferencetermopened',
                'totalevents',
                'distinctproducts']
    for m in metrics:
        cohort_plot(livebook_data_path,m)


if __name__ == "__main__":
    # observations()
    # dataset()
    cohorts()
