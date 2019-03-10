import sqlalchemy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import pandas

schema = 'b'
from_date ='2018-07-01' # broadly end of  bad event data
to_date ='2019-02-01'

# schema = 'v'
# from_date ='2018-04-01'
# to_date ='2019-01-01'

# schema = 'k'
# from_date ='2017-01-08'
# to_date ='2018-01-01'

one_metric='Cost_Local_PerMonth_QAExtreme'
# one_metric='CustomerPromoter_PerMonth'
one_metric=None

hideAx=True
monthFormat = mdates.DateFormatter('%b')


with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
	metric_dict=json.loads(myfile.read())

save_path = '../../../fight-churn-output/' + schema + '/'

engine = sqlalchemy.create_engine("postgres://postgres:churn@localhost/postgres")
conn = engine.connect()

with open('../sql/metric_qa.sql', 'r') as myfile:
	sql = myfile.read().replace('\n', ' ')

for idx, metric in enumerate(metric_dict.keys()):
	if one_metric is not None and metric!=one_metric:
		continue
	print('Checking metric %s' % metric)
	aSql = sql.replace('%metric_name_id',str(idx))
	aSql = aSql.replace('%schema',schema)
	aSql = aSql.replace('%from_date',from_date)
	aSql = aSql.replace('%to_date',to_date)

	# print(aSql)
	res = pandas.read_sql_query(aSql,conn)
	cleanedName = ''.join(e for e in metric if e.isalnum())
	# res.to_csv(save_path+cleanedName+'_metric_qa.csv',index=False)

	plt.figure(figsize=(8,10))
	plt.subplot(4, 1, 1)
	plt.plot('calc_date', 'max_val', data=res, marker='', color='red', linewidth=2, label="max")
	if hideAx: plt.gca().get_xaxis().set_visible(False) # Hiding y axis labels on the count
	plt.ylim(0, round(1.1*res['max_val'].max()))
	plt.legend()
	plt.title(metric)
	plt.subplot(4, 1, 2)
	plt.plot('calc_date', 'avg_val', data=res, marker='', color='green', linewidth=2, label='avg')
	if hideAx: plt.gca().get_xaxis().set_visible(False) # Hiding y axis labels on the count
	plt.ylim(0, round(1.1*res['avg_val'].max()))
	plt.legend()
	plt.subplot(4, 1, 3)
	plt.plot('calc_date', 'min_val', data=res, marker='', color='blue', linewidth=2,label='min')
	if hideAx: plt.gca().get_xaxis().set_visible(False) # Hiding y axis labels on the count
	# plt.ylim(0, round(2*res['min_val'].max()))
	plt.legend()
	plt.subplot(4, 1, 4)
	plt.plot('calc_date', 'n_calc', data=res, marker='', color='black', linewidth=2, label="n_calc")
	plt.ylim(0, round(1.1*res['n_calc'].max()))
	plt.legend()
	if hideAx:
		plt.gca().get_yaxis().set_visible(False) # Hiding y axis labels on the count
		plt.gca().get_xaxis().set_major_formatter(monthFormat)
	plt.savefig(save_path+'metric_valqa_'+cleanedName+'.png')
	plt.close()

