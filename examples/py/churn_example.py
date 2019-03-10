from postgres import Postgres
import json

schema = 'b'
# schema = 'k'
# schema = 'v'

# one_example='listing_4_1_ongoing_active_periods'
one_example='listing_4_2_churned_periods'
# one_example=None

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

			if param_dict[chapter][example].get('mode','run') == 'run':
				db.run(sql)
			elif param_dict[chapter][example].get('mode','run') == 'one':
				res = db.one(sql)
			elif param_dict[chapter][example].get('mode','run') == 'all':
				res = db.all(sql)
