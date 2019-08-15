import sys
from metric_calc import MetricCalculator

'''
####################################################################################################
The main script for calculating Fight Churn With Data metrics in batch: If there are command line arguments, 
use them. Otherwise defaults are hard coded

'''

if __name__ == "__main__":

	schema = 'churnsim9'
	run_mets = None
	# Example of running just a few metrics - uncomment this line...
	# run_mets=['account_tenure','post_per_month']

	if len(sys.argv)>=2:
		schema=sys.argv[1]
	if len(sys.argv)>=3:
		run_mets=sys.argv[2:]

	met_calc = MetricCalculator(schema)
	met_calc.qa_metrics(run_mets)
