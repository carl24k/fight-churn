import sqlalchemy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import pandas
import os


properties = []
one_event = None


# schema = 'b'
# schema = 'v'
schema = 'churnsim2'

# properties = ['quantity','duration']
# one_event='Customer_Promoter_QAExMissing'
# one_event='CustomerPromoter'
# one_event='Cost_Local_QAExtreme'
# one_event='Cost_LD_Canada'


with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
	metric_dict=json.loads(myfile.read())


from_date=metric_dict['date_range']['from_date']
to_date=metric_dict['date_range']['to_date']

hideAx=False
monthFormat = mdates.DateFormatter('%b')


if len(properties)>0:
	property_term = ','.join(['sum(%s) as %s' % (p,p) for p in properties])
	property_term = ', ' + property_term
else:
	property_term=''


save_path = '../../../fight-churn-output/' + schema + '/'
os.makedirs(save_path,exist_ok=True)
engine = sqlalchemy.create_engine("postgres://%s:%s@localhost/%s" % (
	os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))
conn = engine.connect()

events = pandas.read_sql_query("select * from %s.event_type" % schema, conn)

with open('../sql/qa_event.sql', 'r') as myfile:
	sql = myfile.read().replace('\n', ' ')

for idx, event in events.iterrows():
	if one_event is not None and event['event_type_name']!=one_event:
		continue
	print('Checking event %s' %   event['event_type_name'])
	aSql = sql.replace('%event_type_id',str(event['event_type_id']))
	aSql = aSql.replace('%schema',schema)
	aSql = aSql.replace('%from_date',from_date)
	aSql = aSql.replace('%to_date',to_date)
	aSql = aSql.replace('%property_term',property_term)

	# print(aSql)
	res = pandas.read_sql_query(aSql,conn)
	cleanedName = ''.join(e for e in event['event_type_name'] if e.isalnum())
	# res.to_csv(save_path+cleanedName+'_event_qa.csv',index=False)

	if not any(res['n_event'].notnull()):
		print('\t *** No events for %s' % cleanedName)
		continue

	valid_properties=[any(res[p].notnull()) for p in properties]
	n_valid_property=sum([int(v) for v in valid_properties])

	if n_valid_property>0:
		plt.figure(figsize=(5,8))
		plt.subplot(n_valid_property+1, 1, 1)
		plt.plot('event_date', 'n_event', data=res, marker='.', color='black', linewidth=1, label="count")
		plt.legend()
		plt.title('%s' % cleanedName)
		if hideAx:
			plt.gca().get_yaxis().set_visible(False)
			plt.gca().get_xaxis().set_major_formatter(monthFormat)
		for p in range(0,n_valid_property):
			if not valid_properties[p] : continue
			count = sum([int(v) for v in valid_properties[0:p+1]])
			plt.subplot(n_valid_property+1, 1, 1+count)
			plt.plot('event_date', properties[p], data=res, marker='.', color='blue', linewidth=1, label="sum(%s)" % properties[p])
			plt.legend()
			if hideAx:
				plt.gca().get_yaxis().set_visible(False)
				plt.gca().get_xaxis().set_major_formatter(monthFormat)
	else:
		res.plot(kind='line',linestyle="-",marker=".",x='event_date',y='n_event',title='%s n_event' % cleanedName,legend=False,ylim=(0,round(1.1*res['n_event'].max())))
		if hideAx:
			plt.gca().get_yaxis().set_visible(False)
			plt.gca().get_xaxis().set_major_formatter(monthFormat)

	plt.savefig(save_path+'event_qa_'+cleanedName+'.png')
	plt.close()


print('Saving results to %s' % save_path)
