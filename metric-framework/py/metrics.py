from postgres import Postgres
import json

bind_char='%'
schema = 'k'
from_date ='2017-01-01'
to_date ='2017-12-31'

with open('../conf/metrics.json', 'r') as myfile:
	metric_dict=json.loads(myfile.read())

db = Postgres("postgres://postgres:churn@localhost/postgres")
db.run('truncate table %s.metric' % schema)


for idx, metric in enumerate(metric_dict.keys()):
	print('Inserting metric %s' % metric)
	with open('../sql/%s.sql' % metric_dict[metric]['sql'], 'r') as myfile:
		sql=myfile.read().replace('\n', ' ')
	params=metric_dict[metric]
	params['metric_name']=metric
	params['schema']=schema
	params['from_date']=from_date
	params['to_date']=to_date
	params['metric_type_id']=idx
	for p in params.keys():
		sql=sql.replace(bind_char+p,str(params[p]))
	db.run(sql)

