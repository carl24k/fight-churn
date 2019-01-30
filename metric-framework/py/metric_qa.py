import sqlalchemy
import matplotlib.pyplot as plt
import json
import pandas

schema = 'k'

with open('../conf/metrics.json', 'r') as myfile:
	metric_dict=json.loads(myfile.read())

save_path = '../../../output/'

engine = sqlalchemy.create_engine("postgres://postgres:churn@localhost/postgres")
conn = engine.connect()

with open('../sql/metric_qa.sql', 'r') as myfile:
	sql = myfile.read().replace('\n', ' ')

for idx, metric in enumerate(metric_dict.keys()):
	print('Checking metric %s' % metric)
	aSql = sql.replace('%metric_type_id',str(idx))
	aSql = aSql.replace('%schema',schema)

	res = pandas.read_sql_query(aSql,conn)
	res.to_csv(save_path+metric+'_qa.csv',index=False)

	res.plot(kind='line',x='metric_time',y='n_calc',title='%s n_calc' % metric,legend=False,ylim=(0,res['n_calc'].max()))
	plt.savefig(save_path+'countqa_'+metric+'.png')
	plt.close()

	res.plot(kind='line',x='metric_time',y='avg_val',title='%s avg' % metric ,legend=False,ylim=(0,res['avg_val'].max()))
	plt.savefig(save_path+'avgqa_'+metric+'.png')
	plt.close()

