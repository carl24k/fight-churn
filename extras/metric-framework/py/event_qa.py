import sqlalchemy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import pandas
import os
import sys
import argparse

parser = argparse.ArgumentParser()
# Run control arguments
parser.add_argument("--schema", type=str, help="The name of the schema", default='socialnet7')
parser.add_argument("--events", type=str,nargs='*', help="List of events to run (default to all)")
parser.add_argument("--hideax", action="store_true", default=False,help="Hide axis labels")
parser.add_argument("--format", type=str, help="Format to save in", default='png')

class EventChecker:

	def __init__(self,args):
		'''
		EventChecker has the parameters and logic to run the QA query on events. Loads parameter json from the adjacent
		conf directory, which has the  date range for the schema. Makes postgres sqlalchemy with environment variables.
		Select all of the events for this schema into a pandas dataframe, by querying the event_type table.
		If a list of properties was provided, the SQL to run QA on the event properties is also created (see
		make_one_event_sql for how that is used)
		:param schema: string the name of the schema
		:param properties: list of strings, property names ffor the events
		'''


		self.args=args
		self.schema=args.schema
		self.monthFormat = mdates.DateFormatter('%b')

		# Load the metric configuration dictionary
		with open('../conf/%s_metrics.json' % self.schema, 'r') as myfile:
			self.metric_dict=json.loads(myfile.read())

		# get the start/end date from the metric configuration
		self.from_date=self.metric_dict['date_range']['from_date']
		self.to_date=self.metric_dict['date_range']['to_date']

		# make the output path (if necessary)
		self.save_path = '../../../fight-churn-output/' + self.schema + '/'
		os.makedirs(self.save_path,exist_ok=True)

		# Make a sql connection with sqlalchmey
		self.URI=  f"postgresql://localhost/{os.environ['CHURN_DB']}?user={os.environ['CHURN_DB_USER']}&password={os.environ['CHURN_DB_PASS']}"
		print('Saving results to %s' % self.save_path)
		engine = sqlalchemy.create_engine(self.URI)
		self.conn = engine.connect()

		# read the event types from the database
		self.events = pandas.read_sql_query("select * from %s.event_type" % self.schema, self.conn)

		# load the sql template used to make the queries
		with open('../sql/qa_event.sql', 'r') as myfile:
			self.qa_sql = myfile.read().replace('\n', ' ')

		# extra setup, if there are event properties
		if len(self.metric_dict['event_properties']) > 0:
			self.property_term = ','.join(['sum(%s) as %s' % (p, p) for p in self.metric_dict['event_properties']])
			self.property_term = ', ' + self.property_term
		else:
			self.property_term = ''


	def make_one_event_sql(self,event):
		'''
		Fill in the SQL template to make one query string for a named event
		:param event:
		:return:
		'''
		print('Checking event %s' % event['event_type_name'])
		aSql = self.qa_sql.replace('%event_type_id', str(event['event_type_id']))
		aSql = aSql.replace('%schema', self.schema)
		aSql = aSql.replace('%from_date', self.from_date)
		aSql = aSql.replace('%to_date', self.to_date)
		aSql = aSql.replace('%property_term', self.property_term)
		return aSql


	def plot_event_without_properties(self,res,cleanedName):
		'''
		Plot query result for an event that has only a simple count (no properties)
		:param res:
		:param cleanedName:
		:return:
		'''
		res.plot(kind='line', linestyle="-", marker=".", x='event_date', y='n_event', color='black',
				 title='%s n_event' % cleanedName, legend=False, ylim=(0, round(1.1 * res['n_event'].max())))
		if self.args.hideax:
			plt.gca().get_yaxis().set_visible(False)
			plt.gca().get_xaxis().set_major_formatter(self.monthFormat)
		else:
			plt.gcf().autofmt_xdate()

	def plot_event_with_properties(self,res,cleaned_name,valid_properties):
		'''
		Plot result for an event with properties
		:param res: data frame with the result of the query
		:param cleaned_name:  string - if the event name was cleaned of spaces or punctuation, this is it
		:param valid_properties: list of strings, names of any properties in this event
		:return:
		'''

		n_valid_property = sum([int(v) for v in valid_properties])
		plt.figure(figsize=(5, 8))
		plt.subplot(n_valid_property + 1, 1, 1)
		plt.plot('event_date', 'n_event', data=res, marker='.', color='black', linewidth=1, label="count")
		plt.legend()
		plt.title('%s' % cleaned_name)
		if self.args.hideax:
			plt.gca().get_yaxis().set_visible(False)
			plt.gca().get_xaxis().set_major_formatter(self.monthFormat)
		for p in range(0, n_valid_property):
			if not valid_properties[p]: continue
			count = sum([int(v) for v in valid_properties[0:p + 1]])
			plt.subplot(n_valid_property + 1, 1, 1 + count)
			plt.plot('event_date', self.metric_dict['event_properties'][p], data=res, marker='.', color='black', linewidth=1,
					 label="sum(%s)" % self.metric_dict['event_properties'][p])
			plt.legend()
			if self.args.hideax:
				plt.gca().get_yaxis().set_visible(False)
				plt.gca().get_xaxis().set_major_formatter(self.monthFormat)


	def check_one_event_qa(self,event,hideAx=False):
		'''
		Run the query and make the plot to check quality of one event.  First the query is formed with make_one_event_sql,
		and the result is retrieved into a Pandas dataframe.
		:param event:
		:param hideAx:
		:return:
		'''
		aSql = self.make_one_event_sql(event)

		res = pandas.read_sql_query(aSql, self.conn)
		cleaned_name = ''.join(e for e in event['event_type_name'] if e.isalnum())
		# res.to_csv(self.save_path+cleaned_name+'_event_qa.csv',index=False)

		if not any(res['n_event'].notnull()):
			print('\t *** No events for %s' % cleaned_name)
			return

		valid_properties = [any(res[p].notnull()) for p in self.metric_dict['event_properties']]
		n_valid_property = sum([int(v) for v in valid_properties])

		if n_valid_property > 0:
			self.plot_event_with_properties(res,cleaned_name,valid_properties)
		else:
			self.plot_event_without_properties(res,cleaned_name)


		plt.savefig(self.save_path + 'event_qa_' + cleaned_name + '.' + self.args.format)
		plt.close()


	def check_events(self):
		'''
		Check all of the events in a loop, calling check_one_event_qa for each.  If a list of events is provided,
		it only checks the events in the list.
		:param events_2check:
		:return:
		'''

		for idx, event in self.events.iterrows():
			if self.args.events is not None and event['event_type_name'] not in self.args.events:
				continue

			self.check_one_event_qa(event)

'''
####################################################################################################
The main script for quality assurance checks on events

'''

if __name__ == "__main__":

	args, _ = parser.parse_known_args()

	event_check = EventChecker(args)
	event_check.check_events()
