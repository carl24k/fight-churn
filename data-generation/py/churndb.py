

from postgres import Postgres
import os

schema_name='churnsim2'

db = Postgres("postgres://%s:%s@localhost/%s" % (
os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))

tables=['event','subscription','event_type','metric','metric_name','active_period','observation']

print('Creating schema %s (if not exists)...' % schema_name)
db.run('CREATE SCHEMA IF NOT EXISTS %s;' % schema_name)

for t in tables:
    with open('../schema/create_%s.sql' % t, 'r') as sqlfile:
        sql = sqlfile.read().replace('\n', ' ')
    sql=sql.replace('x.','%s.' % schema_name)
    print('Creating table %s (if not exists)' % t)
    db.run(sql)
