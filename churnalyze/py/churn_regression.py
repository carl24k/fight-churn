import argparse
import datetime as dt
from churn_calc import ChurnCalculator

parser = argparse.ArgumentParser()
parser.add_argument("--schema", type=str, help="The name of the schema", default='churnsim2')
parser.add_argument("--asofdt", type=str, help="The date on which to fit the model and start forward predictions", default='2018-09-01')
parser.add_argument("--nogroup", action="store_true", default=False,help="Plot cohorts using scored metrics for all (not just skewed)")


def main(args):
    '''
    Creates churn calculator and runs the logistic regression
    :return: None
    '''

    churn_calc = ChurnCalculator(args.schema)
    churn_calc.fit_logistic_model(fit_asof_dt=dt.datetime.strptime(args.asofdt,'%Y-%m-%d'),groups=not args.nogroup)

if __name__ == "__main__":
    args, _ = parser.parse_known_args()
    main(args)
