import sqlalchemy
import matplotlib.pyplot as plt
import json
import pandas

schema = 'k'
from_date ='2017-01-01'
to_date ='2017-12-31'
# one_metric='avg_photos_loaded'
one_metric=None

with open('../conf/metrics.json', 'r') as myfile:
	metric_dict=json.loads(myfile.read())

save_path = '../../../output/'

engine = sqlalchemy.create_engine("postgres://postgres:churn@localhost/postgres")
conn = engine.connect()

with open('../sql/metric_qa.sql', 'r') as myfile:
	sql = myfile.read().replace('\n', ' ')

for idx, metric in enumerate(metric_dict.keys()):
	if one_metric is not None and metric!=one_metric:
		continue
	print('Checking metric %s' % metric)
	aSql = sql.replace('%metric_type_id',str(idx))
	aSql = aSql.replace('%schema',schema)
	aSql = aSql.replace('%from_date',from_date)
	aSql = aSql.replace('%to_date',to_date)

	res = pandas.read_sql_query(aSql,conn)
	res.to_csv(save_path+metric+'_qa.csv',index=False)

	res.plot(kind='line',x='calc_date',y='n_calc',title='%s n_calc' % metric,legend=False,ylim=(0,round(1.1*res['n_calc'].max())))
	plt.savefig(save_path+'countqa_'+metric+'.png')
	plt.close()

	res.plot(kind='line',x='calc_date',y='avg_val',title='%s avg' % metric ,legend=False,ylim=(0,round(1.1*res['avg_val'].max())))
	plt.savefig(save_path+'avgqa_'+metric+'.png')
	plt.close()

