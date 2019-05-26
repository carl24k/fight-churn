from postgres import Postgres
import json
import os
import sys

bind_char='%'

class MetricCalculator:

	def __init__(self,schema):

		with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
			self.metric_dict = json.loads(myfile.read())

		self.schema=schema
		self.from_date = self.metric_dict['date_range']['from_date']
		self.to_date = self.metric_dict['date_range']['to_date']

		self.db = Postgres("postgres://%s:%s@localhost/%s" % (
			os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))


	def remove_old_metrics_from_db(self, run_mets=None):
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
				id =self.db.one(self.metricIdSql(m))
				if id is not None:
					deletSql="delete from %s.metric where metric_name_id=%d and metric_time between '%s'::timestamp and '%s'::timestamp"  \
						   % (schema,id,self.from_date,self.to_date)
					print('Clearing old values: ' + deletSql)
					self.db.run(deletSql)

	def metricIdSql(self,metric_name):
		return "select metric_name_id from %s.metric_name where metric_name='%s'" % (self.schema, metric_name)

	def add_metric_id(self,metric):
		id = self.db.one(self.metricIdSql( metric))
		if id is None:
			id = self.db.one('select max(metric_name_id)+1 from %s.metric_name' % schema)
			if id is None: id = 0
			insertNameSql = "insert into %s.metric_name (metric_name_id,metric_name) values (%d,'%s')" % (
			schema, id, metric)
			self.db.run(insertNameSql)
			print('Inserted metric %s.%s as id %d' % (schema,metric,id))

		return id


	def run_one_metric_calculation(self,metric):

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
		for p in params.keys():
			sql = sql.replace(bind_char + p, str(params[p]))
		print(sql)

		self.db.run(sql)

	def calculate_metrics(self,run_mets=None):

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

