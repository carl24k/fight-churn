from postgres import Postgres
import json
import pandas as pd
from importlib import import_module
import re
import os
import sys

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print_num_rows=5

flat_metric_bind = 'FLAT_METRIC_SELECT'

def generate_flat_metric_sql(db):
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


def sql_example(param_dict, chapter, example):

    chap_params = param_dict[chapter]['params']

    with open('../%s/%s.sql' % (chapter, example), 'r') as myfile:
        db = Postgres("postgres://%s:%s@localhost/%s" % (os.environ['CHURN_DB_USER'],os.environ['CHURN_DB_PASS'],os.environ['CHURN_DB']))

        sql = "set search_path = '%s'; " % schema;
        sql = sql + myfile.read()

        for p in chap_params.keys():
            if p=='type': continue
            sql = sql.replace(p, chap_params[p])
        param_keys = [p for p in param_dict[chapter][example].keys() if p not in ('listing', 'mode')]
        for p in param_keys:
            sql = sql.replace(p, str(param_dict[chapter][example][p]))
        if flat_metric_bind in sql:
            sql = sql.replace(flat_metric_bind, generate_flat_metric_sql(db))

        print('SQL:\n----------\n'+sql+'\n----------\nRESULT:')
        sql = sql.replace('\n', ' ')

        mode = param_dict[chapter][example]['mode'] if 'mode' in param_dict[chapter][example] else chap_params['mode']
        if mode == 'run':
            db.run(sql)
        elif mode == 'one':
            res = db.one(sql)
            print(res)
        elif mode == 'top' or mode == 'save':
            res = db.all(sql)
            df = pd.DataFrame(res)
            if mode == 'save':
                csv_path=save_path + example + '.csv'
                print('Saving: %s' % csv_path)
                df.to_csv(csv_path, index=False)
            else:
                print(df.head(print_num_rows))

def python_example(param_dict,chapter,example):

    example_name_regexp = 'listing_\\d+_\\d+_(\w+)'

    chap_params = param_dict[chapter]['params']
    example_params = param_dict[chapter][example]
    for k in chap_params.keys():
        if k=='type': continue
        example_params[k]=chap_params[k]

    # mod = import_module(chapter  + '.' + example)
    mod = import_module(example)
    m = re.search(example_name_regexp, example)
    if m:
        ex_name = m.group(1)
        ex_fun = getattr(mod, ex_name)
        ex_fun(**example_params)
    else:
        print('Bad function name')


if __name__ == "__main__":

    schema = 'churnsim2'
    chapter = 4
    listing = 'A'

    if len(sys.argv)==4:
        schema=sys.argv[1]
        chapter=sys.argv[2]
        listing=sys.argv[3]

    save_path = '../../../fight-churn-output/' + schema + '/'
    os.makedirs(save_path,exist_ok=True)

    chapter_key='chap{}'.format(chapter)
    listing_prefix='listing_{c}_{l}_'.format(c=chapter,l=listing)

    conf_path='../conf/%s_examples.json' % schema
    if not os.path.isfile(conf_path):
        print('No params %s to run listings on schema %s' % (conf_path,schema))
        exit(-1)

    with open(conf_path, 'r') as myfile:
        param_dict=json.loads(myfile.read())

    if not chapter_key in param_dict:
        print('No params for chapter %d in %s_examples.json' % (chapter,schema))
        exit(-2)

    found_listing = False
    for listing_name in param_dict[chapter_key].keys():

        if listing_name=='params' or not listing_prefix in listing_name:
            continue

        print('\nRunning %s listing %s on schema %s' % (chapter_key,listing_name,schema))
        found_listing=True
        type = param_dict[chapter_key][listing_name].get('type', param_dict[chapter_key]['params']['type']) # chap params should always have type
        if type=='sql':
            sql_example(param_dict,chapter_key,listing_name)
        elif type=='py':
            python_example(param_dict,chapter_key,listing_name)
        else:
            raise Exception('Unsupported type %s' % type)
        exit(0)

    if not found_listing:
        print('No params for listing %d, chapter %d in %s_examples.json' % (listing,chapter,schema))
        exit(-3)
