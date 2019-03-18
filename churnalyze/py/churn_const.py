

log_scale_skew_thresh=4
key_cols = no_plot = ['account_id', 'observation_date']
out_col = 'is_churn'
no_plot.append(out_col)
save_path_base = '../../../fight-churn-output/'

load_mat_file='load_mat'

schema_data_dict = {
    'b': 'BroadlyDataSet2',
    'v': 'VersatureDataSet1',
    'k': 'KlipfolioDataSet1'
}


def save_path(schema,file_name=None):
    if file_name is None:
        return save_path_base + schema + '/'
    else:
        return save_path_base + schema + '/' + schema_data_dict[schema] + '_' + file_name + '.csv'
