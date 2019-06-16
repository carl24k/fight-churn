# import pandas as pd
import sys
# import matplotlib.pyplot as plt

from churn_calc import ChurnCalculator
# from churn_const import  schema_data_dict


def main():


    schema = 'churnsim2'

    if len(sys.argv) >= 2:
        schema = sys.argv[1]

    churn_calc = ChurnCalculator(schema)
    churn_calc.dataset_stats(save=True)
    churn_calc.dataset_corr(save=True)

if __name__ == "__main__":
    main()
