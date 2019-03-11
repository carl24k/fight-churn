from postgres import Postgres
import json
import pandas as pd

schema = 'b'
# schema = 'k'
# schema = 'v'
save_path = '../../../fight-churn-output/' + schema + '/'

# one_example='listing_4_1_ongoing_active_periods'
one_example='listing_4_5_data_set_create_template'
# one_example=None

flat_metric_bind = 'FLAT_METRIC_SELECT'
flat_metric_template = ', sum(case when metric_name_id=%d then metric_value else 0 end) as %s'

def generate_flat_metric_sql(db):
	res = db.all('select * from %s.metric_name;' % schema)
	sql=''.join( [ flat_metric_template % (row[0], row[1]) for row in res])
	return sql


with open('../conf/%s_examples.json' % schema, 'r') as myfile:
	param_dict=json.loads(myfile.read())

db = Postgres("postgres://postgres:churn@localhost/postgres")

for chapter in param_dict.keys():

	for idx, example in enumerate(param_dict[chapter].keys()):
		if one_example is not None and example != one_example:
			continue
		print('%s %d Running example %s' % (chapter, idx,example))

		listing = param_dict[chapter][example].get('listing',example)
		with open('../%s/%s.sql' % (chapter, listing), 'r') as myfile:
			sql = "set search_path = '%s'; " % schema;
			sql=sql + myfile.read().replace('\n', ' ')

			param_keys = [p for p in param_dict[chapter][example].keys() if p not in ('listing','mode')]
			for p in param_keys:
				sql=sql.replace(p,str(param_dict[chapter][example][p]))
			if flat_metric_bind in sql:
				sql=sql.replace(flat_metric_bind,generate_flat_metric_sql(db))

			if param_dict[chapter][example].get('mode', 'run') == 'run':
				db.run(sql)
			elif param_dict[chapter][example].get('mode', 'run') == 'one':
				res = db.one(sql)
			elif param_dict[chapter][example].get('mode', 'run') == 'all':
				res = db.all(sql)
				df = pd.DataFrame(res)
				print('Saving...')
				df.to_csv(save_path + example + ' .csv')
