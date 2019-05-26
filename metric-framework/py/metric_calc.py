from postgres import Postgres
import json
import os
import sys


class MetricCalculator:

	def __init__(self,schema):
		'''
		Initialize metric calculator from schema name.  Loads parameter json from the adjacent conf directory.
		Loads date range from the configuration. Makes postgres connection with environment variables.
		:param schema:
		'''

		with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
			self.metric_dict = json.loads(myfile.read())

		self.schema=schema
		self.from_date = self.metric_dict['date_range']['from_date']
		self.to_date = self.metric_dict['date_range']['to_date']

		self.db = Postgres("postgres://%s:%s@localhost/%s" % (
			os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))


	def remove_old_metrics_from_db(self, run_mets=None):
		'''
		Delete values of existing metrics. If no metrics are specified, it truncates the metric table. Otherwise
		just delete the specified metrics.
		:param run_mets: list of strings, metric names; or else None meaning truncate all metrics
		:return:
		'''
		if run_mets is None:
			print('TRUNCATING *Metrics* in schema -> %s <-  ...' % schema)
			if input("are you sure? (enter %s to proceed) " % schema) == schema:
				self.db.run('truncate table %s.metric' % schema)
				self.db.run('truncate table %s.metric_name' % schema)
			else:
				exit(0)
		else:
			if isinstance(run_mets,str): run_mets=[run_mets]
			if len(run_mets)>1:
				print('DELETING * %d * Metrics in schema -> %s <-  ...' % (len(run_mets),schema))
				if input("are you sure? (enter %s to proceed) " % schema) != schema:
					exit(0)
			for m in run_mets:
				id =self.get_metric_id(m)
				if id is not None:
					deletSql="delete from %s.metric where metric_name_id=%d and metric_time between '%s'::timestamp and '%s'::timestamp"  \
						   % (schema,id,self.from_date,self.to_date)
					print('Clearing old values: ' + deletSql)
					self.db.run(deletSql)

	def get_metric_id(self,metric_name):
		'''
		Get the id of one metric from the database by name
		:param metric_name: string name of the metric
		:return: id number of the metric, assuming one was found; or else SQL returns NULL as None in Python
		'''
		sql = "select metric_name_id from %s.metric_name where metric_name='%s'" % (self.schema, metric_name)
		return self.db.one(sql)

	def add_metric_id(self,metric):
		'''
		Add an id for a metric if it doesn't already exist
		:param metric: string name of the metric
		:return:
		'''
		id = self.get_metric_id(metric)
		if id is None:
			id = self.db.one('select max(metric_name_id)+1 from %s.metric_name' % schema)
			if id is None: id = 0
			insertNameSql = "insert into %s.metric_name (metric_name_id,metric_name) values (%d,'%s')" % (
			schema, id, metric)
			self.db.run(insertNameSql)
			print('Inserted metric %s.%s as id %d' % (schema,metric,id))

		return id


	def run_one_metric_calculation(self,metric):
		'''
		Calculate one metric, by name.  First adds the id, then loads the raw sql from the file.  To set the bind
		variables it starts out with the second level dictionary for this metric from the main metric dictionary.
		Then it adds all of the metric parameters that are common to all metric calcultions, such as from and to
		 dates, the metric name id, a schema and the value name.  These are put into the SQL template with a simple
		 replace (did not use the Postgres bind system because it was not flexible enough.) Finally, it runs the SQL.
		:param metric: string name of the metric
		:return:
		'''

		assert metric in self.metric_dict, "No metric %s in metric dictionary!" % metric

		id = self.add_metric_id(metric)

		with open('../sql/%s.sql' % self.metric_dict[metric]['sql'], 'r') as myfile:
			sql = myfile.read().replace('\n', ' ')

		params = self.metric_dict[metric]
		params['metric_name_val'] = metric
		params['schema'] = schema
		params['from_date'] = self.from_date
		params['to_date'] = self.to_date
		params['metric_name_id'] = id
		bind_char='%'
		for p in params.keys():
			sql = sql.replace(bind_char + p, str(params[p]))
		print(sql)

		self.db.run(sql)

	def calculate_metrics(self,run_mets=None):
		'''
		Loops over the configured metrics and runs them.  If a list was provided, it only runs the ones in the list.
		:param run_mets: list of strings, metric names; or else None meaning calculate all configured metrics
		:return:
		'''

		for metric in self.metric_dict.keys():
			if (run_mets is not None and metric not in run_mets) or metric == 'date_range':
				continue

			self.run_one_metric_calculation(metric)

'''
####################################################################################################
The main script for calculating Fight Churn With Data metrics in batch: If there are command line arguments, 
use them. Otherwise defaults are hard coded

'''

if __name__ == "__main__":

	schema = 'churnsim2'
	# run_mets = None
	run_mets=['account_tenure','post_per_month']

	if len(sys.argv)>=3:
		schema=sys.argv[1]
		run_mets=sys.argv[2:]

	met_calc = MetricCalculator(schema)
	met_calc.remove_old_metrics_from_db(run_mets)
	met_calc.calculate_metrics(run_mets)

