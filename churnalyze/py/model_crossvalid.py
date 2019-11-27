import argparse
import datetime as dt
from churn_calc import ChurnCalculator

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, help="The model to test: logreg, ranfor, xgb", default=ChurnCalculator.LOGISTIC_REGRESSION)
parser.add_argument("--schema", type=str, help="The name of the schema", default='churnsim2')
parser.add_argument("--nogroup", action="store_true", default=False,help="Plot cohorts using scored metrics for all (not just skewed)")
parser.add_argument("--data", type=str, help="The name of the dataset", default=None)


def main(args):
    '''
    Creates churn calculator and runs the logistic regression
    :return: None
    '''

    churn_calc = ChurnCalculator(args.schema, args.data)
    churn_calc.crossvalidate_churn_model(model_code=args.model,groups=not args.nogroup)

if __name__ == "__main__":
    args, _ = parser.parse_known_args()
    main(args)
