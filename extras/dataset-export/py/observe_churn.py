
import os
import pandas as pd
from postgres import Postgres
from run_churn_listing import run_listing_from_args
import argparse

METRIC_BIND = 'FLAT_METRIC_SELECT'
FRBIND = '%from_yyyy-mm-dd'
TOBIND = '%to_yyyy-mm-dd'
INTBIND = '%metric_interval'

def remove_obsevations(schema):
    '''
    Truncate the active period and observtions tables to prepare for a new dataset generation
    :param schema:
    :return:
    '''
    print('Removing old active_period and observation entries...')
    con_string = f"postgresql://localhost/{os.environ['CHURN_DB']}?user={os.environ['CHURN_DB_USER']}&password={os.environ['CHURN_DB_PASS']}"
    db = Postgres(con_string)
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
    parser.add_argument("--dataset", action="store_true", default=False, help="Only resample metrics, not observation dates")
    parser.add_argument("--current", action="store_true", default=False, help="Select a current observation data set")

    args, _ = parser.parse_known_args()
    argd = vars(args)

    if not args.dataset and not args.current:
        # Clean up any data from old runs
        remove_obsevations(args.schema)

        # Create active periods and observations using the exact listings from the book
        # You must configure these with a JSON in listings/conf/<schema>_listings.json
        argd['chapter']=4
        argd['insert']=False
        argd['version']=None
        argd['listing']=1
        run_listing_from_args(args)
        argd['listing']=2
        run_listing_from_args(args)
        argd['listing']=4
        run_listing_from_args(args)

    # Load the base SQL from the adjacent sql directory
    sql = "set search_path = '%s'; " % args.schema;

    if not args.current:
        path ='../sql/export_dataset.sql'
    else:
        path = '../sql/export_dataset_current.sql'

    with open(path , 'r') as myfile:
        sql += myfile.read()

    # Fill in the standard bind parameters with the arguments
    sql = sql.replace(FRBIND,args.frdt)
    sql = sql.replace(TOBIND,args.todt)
    sql = sql.replace(INTBIND,args.interval)

    # Generate the SQL that flattens the metrics (KEY STEP)
    con_string = f"postgresql://localhost/{os.environ['CHURN_DB']}?user={os.environ['CHURN_DB_USER']}&password={os.environ['CHURN_DB_PASS']}"
    db = Postgres(con_string)
    sql = sql.replace(METRIC_BIND, generate_flat_metric_sql(db, args.schema))
    print('EXPORT SQL:\n----------\n' + sql + '\n----------\n')
    sql = sql.replace('\n', ' ')

    # Execute the query and get the result into a data frame
    res = db.all(sql)
    df = pd.DataFrame(res)

    # Save to a csv
    save_path = '../../../fight-churn-output/' + args.schema + '/'
    os.makedirs(save_path,exist_ok=True)
    if not args.current:
        csv_path=save_path +  args.schema + '_dataset.csv'
    else:
        csv_path=save_path +  args.schema + '_dataset_current.csv'

    print('Saving: %s' % csv_path)
    df.to_csv(csv_path, index=False)