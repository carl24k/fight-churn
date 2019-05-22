from postgres import Postgres
import json
from metric_util import metricIdSql
import os

bind_char='%'


schema='churnsim2'

run_mets=None
# run_mets=['account_tenure','post_per_month']



with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
	metric_dict=json.loads(myfile.read())


from_date=metric_dict['date_range']['from_date']
to_date=metric_dict['date_range']['to_date']

db = Postgres("postgres://%s:%s@localhost/%s" % (
os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))

if run_mets is None:
	print('TRUNCATING *Metrics* in schema -> %s <-  ...' % schema)
	if input("are you sure? (enter %s to proceed) " % schema) == schema:
		db.run('truncate table %s.metric' % schema)
		db.run('truncate table %s.metric_name' % schema)
	else:
		exit(0)
else:
	if isinstance(run_mets,str): run_mets=[run_mets]
	if len(run_mets)>1:
		print('DELETING * %d * Metrics in schema -> %s <-  ...' % (len(run_mets),schema))
		if input("are you sure? (enter %s to proceed) " % schema) != schema:
			exit(0)
	for m in run_mets:
		id =db.one(metricIdSql(schema,m))
		if id is not None:
			deletSql="delete from %s.metric where metric_name_id=%d and metric_time between '%s'::timestamp and '%s'::timestamp"  \
				   % (schema,id,from_date,to_date)
			print('Clearing old values: ' + deletSql)
			db.run(deletSql)


for metric in metric_dict.keys():
	if (run_mets is not None and metric not in run_mets) or metric == 'date_range':
		continue

	id = db.one(metricIdSql(schema, metric))
	if id is None:
		id=db.one('select max(metric_name_id)+1 from %s.metric_name' % schema)
		if id is None: id=0
		insertNameSql = "insert into %s.metric_name (metric_name_id,metric_name) values (%d,'%s')" % (schema,id,metric)
		db.run(insertNameSql)

	print('Inserting metric %s.%s as id %d' % (schema,metric,id))
	with open('../sql/%s.sql' % metric_dict[metric]['sql'], 'r') as myfile:
		sql=myfile.read().replace('\n', ' ')
	params=metric_dict[metric]
	params['metric_name_val']=metric
	params['schema']=schema
	params['from_date']=from_date
	params['to_date']=to_date
	params['metric_name_id']=id
	for p in params.keys():
		sql=sql.replace(bind_char+p,str(params[p]))
	print(sql)

	db.run(sql)

