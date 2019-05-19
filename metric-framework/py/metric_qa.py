import sqlalchemy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import pandas
from math import ceil
import os

from metric_util import metricIdSql
from schema_const import schema_data_dict

run_mets=None

# schema = 'b'
# schema = 'v'
# schema = 'k'
schema = 'churnsim2'

# run_mets='Cost_Local_PerMonth_QAExtreme'
# run_mets='CustomerPromoter_PerMonth'
# run_mets='mrr'
# run_mets = ['klips_per_tab','data_sources_per_tab','time_per_edit','dashboard_views_per_day','edits_per_view']
# run_mets=['Klips_Owned_Average','klips_per_tab']
# run_mets=['extension_units','base_units','mrr']
# run_mets=['num_seats','num_api_calls','num_dashboards','num_privatelink','mrr']
# run_mets=['Cost_Local_PerMonth','Cost_LD_Canada_PerMonth','Cost_Toll_Free_PerMonth','Cost_LD_US_PerMonth','Cost_International_PerMonth']
# run_mets='mrr'
# run_mets=['Cost_LD_Canada_PerMonth','Cost_Toll_Free_PerMonth','Cost_LD_US_PerMonth','Cost_International_PerMonth']
# run_mets='Total_Use_Per_Month'
# run_mets=['Use_Per_Base_Unit','Use_Per_Dollar_MRR','Percent_Canada','Percent_US','Percent_Intl','Percent_TollFree','Dollar_MRR_Per_Call_Unit','Dollar_MRR_Per_Base_Unit']
# run_mets = ['Active_Users_Last_Qtr']
# run_mets=['active_users_per_seat','active_users_per_dollar_mrr','dollars_per_dashboard','dashboards_per_dollar_mrr','dash_views_per_user_per_month']
# run_mets=['billing_period']
# run_mets=['num_users']
# run_mets=['Total_Tractors_Per_Month','Detractor_Rate','Promoter_Rate']
# run_mets=['User_Utilization']

hideAx=False
monthFormat = mdates.DateFormatter('%b')

from_date=schema_data_dict[schema]['from_date']
to_date=schema_data_dict[schema]['to_date']

with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
	metric_dict=json.loads(myfile.read())

save_path = '../../../fight-churn-output/' + schema + '/'


engine = sqlalchemy.create_engine("postgres://%s:%s@localhost/%s" % (
	os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))
conn = engine.connect()

with open('../sql/qa_metric.sql', 'r') as myfile:
	sql = myfile.read().replace('\n', ' ')

for idx, metric in enumerate(metric_dict.keys()):
	if run_mets is not None and metric not in run_mets:
		continue
	print('Checking metric %s.%s' % (schema,metric))
	id = pandas.read_sql_query(metricIdSql(schema, metric),conn)
	aSql = sql.replace('%metric_name_id',str(id['metric_name_id'][0]))
	aSql = aSql.replace('%schema',schema)
	aSql = aSql.replace('%from_date',from_date)
	aSql = aSql.replace('%to_date',to_date)

	# print(aSql)
	res = pandas.read_sql_query(aSql,conn)
	if res.shape[0]==0 or res['avg_val'].isnull().values.all():
		print('\t*** No result for %s' % metric)
		continue

	cleanedName = ''.join(e for e in metric if e.isalnum())
	# res.to_csv(save_path+cleanedName+'_metric_qa.csv',index=False) # uncomment to save details


	plt.figure(figsize=(8,10))
	plt.subplot(4, 1, 1)
	plt.plot('calc_date', 'max_val', data=res, marker='', color='red', linewidth=2, label="max")
	if hideAx: plt.gca().get_xaxis().set_visible(False) # Hiding y axis labels on the count
	plt.ylim(0, ceil(1.1*res['max_val'].dropna().max()))
	plt.legend()
	plt.title(metric)
	plt.subplot(4, 1, 2)
	plt.plot('calc_date', 'avg_val', data=res, marker='', color='green', linewidth=2, label='avg')
	if hideAx: plt.gca().get_xaxis().set_visible(False) # Hiding y axis labels on the count
	plt.ylim(0, ceil(1.1*res['avg_val'].dropna().max()))
	plt.legend()
	plt.subplot(4, 1, 3)
	plt.plot('calc_date', 'min_val', data=res, marker='', color='blue', linewidth=2,label='min')
	if hideAx: plt.gca().get_xaxis().set_visible(False) # Hiding y axis labels on the count
	# plt.ylim(0, ceil(2*res['min_val'].dropna().max()))
	plt.legend()
	plt.subplot(4, 1, 4)
	plt.plot('calc_date', 'n_calc', data=res, marker='', color='black', linewidth=2, label="n_calc")
	plt.ylim(0, ceil(1.1*res['n_calc'].dropna().max()))
	plt.legend()
	if hideAx:
		plt.gca().get_yaxis().set_visible(False) # Hiding y axis labels on the count
		plt.gca().get_xaxis().set_major_formatter(monthFormat)
	plt.savefig(save_path+'metric_valqa_'+cleanedName+'.png')
	plt.close()

