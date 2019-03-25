from postgres import Postgres
import json
from metric_util import metricIdSql
from schema_const import schema_data_dict

bind_char='%'
run_mets=None

# schema = 'b'
# schema = 'v'
schema = 'k'

# run_mets='Cost_Local_PerMonth_QAExtreme'
# run_mets=['account_tenure','mrr']
# run_mets=['base_units','extension_units']
# run_mets=['num_privatelink','num_api_calls','num_dashboards','num_seats']
# run_mets=['Cost_Local_PerMonth','Cost_LD_Canada_PerMonth','Cost_Toll_Free_PerMonth','Cost_LD_US_PerMonth','Cost_International_PerMonth']
# run_mets='Total_Use_Per_Month'
# run_mets=['Use_Per_Base_Unit','Use_Per_Dollar_MRR','Percent_Canada','Percent_US','Percent_Intl','Percent_TollFree','Dollar_MRR_Per_Call_Unit','Dollar_MRR_Per_Base_Unit']
run_mets=['billing_period']
# run_mets=['active_users_per_seat','active_users_per_dollar_mrr','dollars_per_dashboard','dashboards_per_dollar_mrr','dash_views_per_user_per_month','editor_time_per_user']
# run_mets=['Customer_added_Per_Dollar','CustomerPromoter_Per_Dollar','Contact_Per_Dollar','Transactions_Per_Dollar','Message_Viewed_Per_Dollar']

from_date=schema_data_dict[schema]['from_date']
to_date=schema_data_dict[schema]['to_date']

with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
	metric_dict=json.loads(myfile.read())

db = Postgres("postgres://postgres:churn@localhost/postgres")
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
	if run_mets is not None and metric not in run_mets:
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

