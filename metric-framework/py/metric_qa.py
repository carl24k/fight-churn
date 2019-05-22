import sqlalchemy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import pandas
from math import ceil
import os

from metric_util import metricIdSql

# schema = 'b'
# schema = 'v'
# schema = 'k'
schema = 'churnsim2'

run_mets=None
# run_mets=['account_tenure','post_per_month']

hideAx=False
monthFormat = mdates.DateFormatter('%b')

with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
	metric_dict=json.loads(myfile.read())

from_date=metric_dict['date_range']['from_date']
to_date=metric_dict['date_range']['to_date']

save_path = '../../../fight-churn-output/' + schema + '/'
os.makedirs(save_path,exist_ok=True)


engine = sqlalchemy.create_engine("postgres://%s:%s@localhost/%s" % (
	os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))
conn = engine.connect()

with open('../sql/qa_metric.sql', 'r') as myfile:
	sql = myfile.read().replace('\n', ' ')

for idx, metric in enumerate(metric_dict.keys()):
	if (run_mets is not None and metric not in run_mets)  or metric == 'date_range':
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


print('Saving results to %s' % save_path)
