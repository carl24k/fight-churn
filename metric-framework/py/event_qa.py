import sqlalchemy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import pandas
import os
import sys


class EventChecker:

	def __init__(self,schema,properties=[]):

		with open('../conf/%s_metrics.json' % schema, 'r') as myfile:
			self.metric_dict=json.loads(myfile.read())

		self.schema=schema
		self.from_date=self.metric_dict['date_range']['from_date']
		self.to_date=self.metric_dict['date_range']['to_date']

		self.save_path = '../../../fight-churn-output/' + schema + '/'
		os.makedirs(self.save_path,exist_ok=True)

		self.URI="postgres://%s:%s@localhost/%s" % (
			os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB'])
		print('Saving results to %s' % self.save_path)
		engine = sqlalchemy.create_engine(self.URI)
		self.conn = engine.connect()

		self.events = pandas.read_sql_query("select * from %s.event_type" % schema, self.conn)

		with open('../sql/qa_event.sql', 'r') as myfile:
			self.qa_sql = myfile.read().replace('\n', ' ')

		if len(properties) > 0:
			self.property_term = ','.join(['sum(%s) as %s' % (p, p) for p in properties])
			self.property_term = ', ' + self.property_term
		else:
			self.property_term = ''

	def make_one_event_sql(self,event):
		print('Checking event %s' % event['event_type_name'])
		aSql = self.qa_sql.replace('%event_type_id', str(event['event_type_id']))
		aSql = aSql.replace('%schema', self.schema)
		aSql = aSql.replace('%from_date', self.from_date)
		aSql = aSql.replace('%to_date', self.to_date)
		aSql = aSql.replace('%property_term', self.property_term)
		return aSql

	def check_one_event_qa(self,event,hideAx=False):
		aSql = self.make_one_event_sql(event)

		# print(aSql)
		res = pandas.read_sql_query(aSql, self.conn)
		cleanedName = ''.join(e for e in event['event_type_name'] if e.isalnum())
		# res.to_csv(save_path+cleanedName+'_event_qa.csv',index=False)

		if not any(res['n_event'].notnull()):
			print('\t *** No events for %s' % cleanedName)
			return

		valid_properties = [any(res[p].notnull()) for p in properties]
		n_valid_property = sum([int(v) for v in valid_properties])

		monthFormat = mdates.DateFormatter('%b')

		if n_valid_property > 0:
			plt.figure(figsize=(5, 8))
			plt.subplot(n_valid_property + 1, 1, 1)
			plt.plot('event_date', 'n_event', data=res, marker='.', color='black', linewidth=1, label="count")
			plt.legend()
			plt.title('%s' % cleanedName)
			if hideAx:
				plt.gca().get_yaxis().set_visible(False)
				plt.gca().get_xaxis().set_major_formatter(monthFormat)
			for p in range(0, n_valid_property):
				if not valid_properties[p]: continue
				count = sum([int(v) for v in valid_properties[0:p + 1]])
				plt.subplot(n_valid_property + 1, 1, 1 + count)
				plt.plot('event_date', properties[p], data=res, marker='.', color='blue', linewidth=1,
						 label="sum(%s)" % properties[p])
				plt.legend()
				if hideAx:
					plt.gca().get_yaxis().set_visible(False)
					plt.gca().get_xaxis().set_major_formatter(monthFormat)
		else:
			res.plot(kind='line', linestyle="-", marker=".", x='event_date', y='n_event',
					 title='%s n_event' % cleanedName, legend=False, ylim=(0, round(1.1 * res['n_event'].max())))
			if hideAx:
				plt.gca().get_yaxis().set_visible(False)
				plt.gca().get_xaxis().set_major_formatter(monthFormat)

		plt.savefig(self.save_path + 'event_qa_' + cleanedName + '.png')
		plt.close()

	def check_events(self,events_2check=None):

		for idx, event in self.events.iterrows():
			if events_2check is not None and event['event_type_name'] not in events_2check:
				continue

			self.check_one_event_qa(event)

'''
####################################################################################################
The main script for calculating Fight Churn With Data metrics in batch: If there are command line arguments, 
use them. Otherwise defaults are hard coded

'''

if __name__ == "__main__":

	schema = 'churnsim2'

	properties = []
	# properties = ['quantity','duration']

	schema = 'churnsim2'
	events_2check = None
	# Example of running just a few events - uncomment this line...
	events_2check=['post','like']

	if len(sys.argv)>=2:
		schema=sys.argv[1]
	if len(sys.argv)>=3:
		events_2check=sys.argv[2:]

	event_check = EventChecker(schema,properties)
	event_check.check_events(events_2check)
