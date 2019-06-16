import sys

from churn_calc import ChurnCalculator


def main():


    schema = 'churnsim2'

    if len(sys.argv) >= 2:
        schema = sys.argv[1]

    churn_calc = ChurnCalculator(schema)
    churn_calc.dataset_stats(save=True)
    churn_calc.dataset_corr(save=True)

if __name__ == "__main__":
    main()
