import sys
from metric_calc import MetricCalculator

import argparse

parser = argparse.ArgumentParser()
# Run control arguments
parser.add_argument("--schema", type=str, help="The name of the schema", default='socialnet7')
parser.add_argument("--metrics", type=str,nargs='*', help="List of metrics to run (default to all)")
parser.add_argument("--hideax", action="store_true", default=False,help="Hide axis labels")
parser.add_argument("--format", type=str, help="Format to save in", default='png')

'''
####################################################################################################
The main script for calculating Fight Churn With Data metrics in batch

'''

if __name__ == "__main__":

	args, _ = parser.parse_known_args()

	met_calc = MetricCalculator(args.schema)
	met_calc.qa_metrics(args)
