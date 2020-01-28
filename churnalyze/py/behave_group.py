
import sys

from churn_calc import  ChurnCalculator


def main():
    '''
    Creates churn calculator and runs the behavior grouping analysis function.
    The schema name is taken from the first command line argument.
    The dataset and all other parameters are then taken from the schema configuration.
    :return: None
    '''
    schema = 'socialnet7'
    data=None
    if len(sys.argv) >= 2:
        schema = sys.argv[1]
    if len(sys.argv) >= 3:
        data = sys.argv[2]

    churn_calc = ChurnCalculator(schema,data)

    churn_calc.calc_behavior_groups()

if __name__ == "__main__":

    main()
