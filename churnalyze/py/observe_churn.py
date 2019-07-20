
import sys
import os
from postgres import Postgres
from run_churn_listing import run_one_listing

def remove_obsevations(schema):
    print('Removing old active_period and observation entries...')
    db = Postgres("postgres://%s:%s@localhost/%s" % (
        os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))
    db.run('truncate table %s.active_period' % schema)
    db.run('truncate table %s.observation' % schema)

if __name__ == "__main__":

    schema = 'churnsim2'

    if len(sys.argv)==2:
        schema=sys.argv[1]

    remove_obsevations(schema)

    run_one_listing(schema,4,1)
    run_one_listing(schema,4,2)
    run_one_listing(schema,4,4)
    run_one_listing(schema,4,'A')
