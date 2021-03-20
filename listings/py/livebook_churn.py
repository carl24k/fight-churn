from listing_5_1_cohort_plot import cohort_plot
from listing_5_2_dataset_stats import dataset_stats
from listing_6_2_dataset_correlation_matrix import dataset_correlation_matrix
from listing_3_7_metric_qa_plot import metric_qa_plot

from run_churn_listing import sql_listing

livebook_data_path = '../../../fight-churn-output/livebook/livebook_dataset.csv'

def observations():
    sql_listing(4, 8, 'livebook_observations', 'livebook', mode='run', param_dict={})

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

def readingUtilities():
    params = {
        "%from_yyyy-mm-dd": "2019-12-01",
        "%to_yyyy-mm-dd": "2020-06-01",
        "%new_metric_id" : 10,
        "%new_metric_name" :'reading_utilities_90d',
        '%metric_list' : "'ReadingFreePreview_90d','HighlightCreated_90d',  'FreeContentCheckout_90d','ReadingOpenChapter_90d', 'WishlistItemAdded_90d','CrossReferenceTermOpened_90d'"
    }
    sql_listing(7, 3, 'total_metric', 'livebook', mode='run', param_dict=params, insert=True)


def ratio1():
    params = {
        "%from_yyyy-mm-dd": "2019-12-01",
        "%to_yyyy-mm-dd": "2020-06-01",
        "%new_metric_id" : 11,
        "%new_metric_name" :'downloads_per_book',
        '%num_metric' : 'EBookDownloaded_90d',
        '%den_metric' :'DistinctProducts'
    }
    sql_listing(7,1,'ratio_metric','livebook',mode='run',param_dict=params,insert=True)

def percent_reading():
    params = {
        "%from_yyyy-mm-dd": "2019-12-01",
        "%to_yyyy-mm-dd": "2020-06-01",
        "%new_metric_id" : 12,
        "%new_metric_name" :'percent_reading',
        '%num_metric' : 'ReadingOwnedBook_90d',
        '%den_metric' :'TotalEvents_90d'
    }
    sql_listing(7,1,'ratio_metric','livebook',mode='run',param_dict=params,insert=True)


def percent_utilities():
    params = {
        "%from_yyyy-mm-dd": "2019-12-01",
        "%to_yyyy-mm-dd": "2020-06-01",
        "%new_metric_id" : 13,
        "%new_metric_name" :'percent_utilities',
        '%num_metric' : 'reading_utilities_90d',
        '%den_metric' :'TotalEvents_90d'
    }
    sql_listing(7,1,'ratio_metric','livebook',mode='run',param_dict=params,insert=True)


def events_per_product():
    params = {
        "%from_yyyy-mm-dd": "2019-12-01",
        "%to_yyyy-mm-dd": "2020-06-01",
        "%new_metric_id" : 14,
        "%new_metric_name" :'events_per_product',
        '%num_metric' : 'TotalEvents_90d',
        '%den_metric' :'DistinctProducts'
    }
    sql_listing(7,1,'ratio_metric','livebook',mode='run',param_dict=params,insert=True)


def more_cohorts():
    cohort_plot(livebook_data_path,'reading_utilities')
    cohort_plot(livebook_data_path,'downloads_per_book')
    cohort_plot(livebook_data_path,'percent_reading')
    cohort_plot(livebook_data_path,'percent_utilities')
    cohort_plot(livebook_data_path,'events_per_book')



if __name__ == "__main__":
    # observations()
    # dataset()
    # cohorts()
    # readingUtilities()
    # ratio1()
    # percent_reading()
    # percent_utilities()
    # dataset()
    # more_cohorts()
    # events_per_product()
    dataset_correlation_matrix(livebook_data_path)