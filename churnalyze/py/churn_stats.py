# import pandas as pd
import sys
# import matplotlib.pyplot as plt

from churn_calc import ChurnCalculator
# from churn_const import  schema_data_dict


def main():


    schema = 'churnsim2'
    run_mets = None
    # Example of running just a few metrics - uncomment this line...
    # run_mets=['account_tenure','post_per_month']

    if len(sys.argv) >= 2:
        schema = sys.argv[1]

    churn_calc = ChurnCalculator(schema)
    churn_calc.dataset_stats(churn_calc.save_path('stats'))

    # stat_columns = cc.churn_metric_columns(churn_data.columns.values)
    #
    # summary = cc.dataset_stats(churn_data,stat_columns, save_path=schema_save_path)
    #
    # data_scores, skewed_columns = cc.normalize_skewscale(churn_data, stat_columns, summary)
    #
    # corr = data_scores.corr()
    #
    # corr.to_csv(schema_save_path + '_corr.csv')


if __name__ == "__main__":
    main()
