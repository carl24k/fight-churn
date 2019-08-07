
import os
import pandas as pd
from postgres import Postgres
from run_churn_listing import run_one_listing
import argparse

METRIC_BIND = 'FLAT_METRIC_SELECT'
FRBIND = 'FRYR-MM-DD'
TOBIND = 'TOYR-MM-DD'
INTBIND = 'MET_INTERVAL'

def remove_obsevations(schema):
    print('Removing old active_period and observation entries...')
    db = Postgres("postgres://%s:%s@localhost/%s" % (
        os.environ['CHURN_DB_USER'], os.environ['CHURN_DB_PASS'], os.environ['CHURN_DB']))
    db.run('truncate table %s.active_period' % schema)
    db.run('truncate table %s.observation' % schema)

def generate_flat_metric_sql(db, schema):
    '''
    Helper function for saving a data set for analysis. This flattens the metrics table to form a data set and it
    needs to add a sql clause for every metric in the schema.  This does that by actually querying the metric, table,
    and constructing the sql from a table.
    :param db:
    :return:
    '''

    flat_metric_template = ', sum(case when metric_name_id=%d then metric_value else 0 end) as %s'

    res = db.all('select * from %s.metric_name;' % schema)
    sql=''.join( [ flat_metric_template % (row[0], row[1]) for row in res])
    return sql


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=str, help="The name of the schema", default='churnsim2')
    parser.add_argument("--frdt", type=str, help="Earliest date to export", default='2019-03-04')
    parser.add_argument("--todt", type=str, help="Latest date to export", default='2019-05-06')
    parser.add_argument("--interval", type=str, help="Interval between metrics", default='7 day')
    args, _ = parser.parse_known_args()

    remove_obsevations(args.schema)

    run_one_listing(args.schema,4,1)
    run_one_listing(args.schema,4,2)
    run_one_listing(args.schema,4,4)

    sql = "set search_path = '%s'; " % args.schema;
    with open('../sql/export_dataset.sql' , 'r') as myfile:
        sql += myfile.read()

    sql = sql.replace(FRBIND,args.frdt)
    sql = sql.replace(TOBIND,args.todt)
    sql = sql.replace(INTBIND,args.interval)

    db = Postgres("postgres://%s:%s@localhost/%s" % (os.environ['CHURN_DB_USER'],os.environ['CHURN_DB_PASS'],os.environ['CHURN_DB']))
    sql = sql.replace(METRIC_BIND, generate_flat_metric_sql(db, args.schema))
    print('EXPORT SQL:\n----------\n' + sql + '\n----------\n')
    sql = sql.replace('\n', ' ')

    res = db.all(sql)
    df = pd.DataFrame(res)

    save_path = '../../../fight-churn-output/' + args.schema + '/'
    os.makedirs(save_path,exist_ok=True)
    csv_path=save_path +  args.schema + '_dataset.csv'
    print('Saving: %s' % csv_path)
    df.to_csv(csv_path, index=False)