import sys

from churn_calc import ChurnCalculator


def main():
    '''
    Creates churn calculator and runs the statistics and correlation functions.
    The schema name is taken from the first command line argument.
    The dataset and all other parameters are then taken from the schema configuration.
    :return: None
    '''

    schema = 'churnsim2'

    if len(sys.argv) >= 2:
        schema = sys.argv[1]

    dataset = None
    if len(sys.argv) >= 3:
        dataset = sys.argv[2]

    churn_calc = ChurnCalculator(schema,dataset)
    churn_calc.dataset_stats(save=True)
    churn_calc.dataset_corr(save=True)
    churn_calc.dataset_corr(save=True,use_scores=False)

if __name__ == "__main__":
    main()
