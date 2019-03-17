import pandas as pd
import matplotlib.pyplot as plt

import churn_calc as cc
from churn_const import save_path, key_cols, no_plot, schema_data_dict

# schema = 'b'
# schema = 'v'
schema = 'k'

data_file = schema_data_dict[schema]
schema_save_path = save_path(schema)+data_file


def main():
    churn_data = pd.read_csv(schema_save_path+'.csv',index_col=0)
    print('Loaded %s, size=%dx%d with columns:' % (data_file,churn_data.shape[0],churn_data.shape[1]))
    stat_columns = cc.churn_metric_columns(churn_data.columns.values)

    summary = cc.dataset_stats(churn_data,stat_columns, save_path=schema_save_path)

    data_scores, skewed_columns = cc.normalize_skewscale(churn_data, stat_columns, summary)

    corr = data_scores.corr()

    corr.to_csv(schema_save_path + '_corr.csv')


if __name__ == "__main__":
    main()
