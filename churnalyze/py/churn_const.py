

log_scale_skew_thresh=4
key_cols = no_plot = ['account_id', 'observation_date']
out_col = 'is_churn'
no_plot.append(out_col)
save_path_base = '../../../fight-churn-output/'

schema_data_dict = {
    'b': 'BroadlyDataSet1',
    'v': 'VersatureDataSet1',
    'k': 'KlipfolioDataSet1'
}

def save_path(schema):
    return save_path_base + schema + '/'

