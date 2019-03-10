from postgres import Postgres
import json

bind_char='%'

# schema = 'b'
# from_date ='2018-07-01' # broadly end of  bad event data
# to_date ='2019-03-01'

# schema = 'v'
# from_date ='2018-04-01'
# to_date ='2019-02-26'
# one_metric='Cost_Local_PerMonth_QAExtreme'

schema = 'k'
from_date ='2017-01-08'
to_date ='2018-01-01'
one_metric='Download_PerMonth_26Week'


# one_metric='account_tenure'
# one_metric=None

with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
	metric_dict=json.loads(myfile.read())

db = Postgres("postgres://postgres:churn@localhost/postgres")
if one_metric is None:
	print('TRUNCATING *Metrics* in schema -> %s <-  ...' % schema)
	if input("are you sure? (enter %s to proceed) " % schema) == schema:
		db.run('truncate table %s.metric' % schema)
		db.run('truncate table %s.metric_name' % schema)
	else:
		exit(0)


for idx, metric in enumerate(metric_dict.keys()):
	if one_metric is not None and metric != one_metric:
		continue
	print('%d Inserting metric %s' % (idx,metric))
	with open('../sql/%s.sql' % metric_dict[metric]['sql'], 'r') as myfile:
		sql=myfile.read().replace('\n', ' ')
	params=metric_dict[metric]
	params['metric_name_val']=metric
	params['schema']=schema
	params['from_date']=from_date
	params['to_date']=to_date
	params['metric_name_id']=idx
	for p in params.keys():
		sql=sql.replace(bind_char+p,str(params[p]))
	# print(sql)
	db.run(sql)

