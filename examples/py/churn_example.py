from postgres import Postgres
import json
import pandas as pd
from importlib import import_module
from copy import copy
import re
import os
import sys


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print_num_rows=5


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


def sql_example(param_dict):

    flat_metric_bind = 'FLAT_METRIC_SELECT'

    with open('../chap%d/%s.sql' % (param_dict['chapter'], param_dict['name']), 'r') as myfile:
        db = Postgres("postgres://%s:%s@localhost/%s" % (os.environ['CHURN_DB_USER'],os.environ['CHURN_DB_PASS'],os.environ['CHURN_DB']))

        sql = "set search_path = '%s'; " % param_dict['schema'];
        sql = sql + myfile.read()

        param_keys = [p for p in param_dict.keys() if p not in ('listing', 'mode','type')]
        for p in param_keys:
            sql = sql.replace(p, str(param_dict[p]))
        if flat_metric_bind in sql:
            sql = sql.replace(flat_metric_bind, generate_flat_metric_sql(db,param_dict['schema']))

        print('SQL:\n----------\n'+sql+'\n----------\nRESULT:')
        sql = sql.replace('\n', ' ')

        if  param_dict['mode']  == 'run':
            db.run(sql)
        elif  param_dict['mode']  == 'one':
            res = db.one(sql)
            print(res)
        elif  param_dict['mode']  == 'top' or param_dict['mode'] == 'save':
            res = db.all(sql)
            df = pd.DataFrame(res)
            if  param_dict['mode']  == 'save':
                save_path = '../../../fight-churn-output/' + param_dict['schema'] + '/'
                os.makedirs(save_path,exist_ok=True)
                csv_path=save_path +  param_dict['name']  + '.csv'
                print('Saving: %s' % csv_path)
                df.to_csv(csv_path, index=False)
            else:
                print(df.head(print_num_rows))
        else:
            print('Unknown run mode for SQL example')
            exit(-4)


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

def load_and_check_listing_params(schema, chapter, listing):

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

    listing_params = copy(param_dict[chapter_key]['params'])

    for listing_name in param_dict[chapter_key].keys():

        if listing_name=='params' or not listing_prefix in listing_name:
            continue

        listing_params['schema'] = schema
        listing_params['name'] = listing_name
        listing_params['chapter']=chapter
        listing_params['listing']=listing
        if len(param_dict[chapter_key][listing_name])>0:
            for k in param_dict[chapter_key][listing_name].keys():
                listing_params[k]=param_dict[chapter_key][listing_name][k]

        return listing_params

    print('No params for listing %d, chapter %d in %s_examples.json' % (listing,chapter,schema))
    exit(-3)


if __name__ == "__main__":

    schema = 'churnsim2'
    chapter = 2
    listing = 1

    if len(sys.argv)==4:
        schema=sys.argv[1]
        chapter=sys.argv[2]
        listing=sys.argv[3]

    listing_params = load_and_check_listing_params(schema,chapter,listing)

    print('\nRunning %d listing %s on schema %s' % (chapter,listing_params['name'],schema))

    type = listing_params.get('type', listing_params['type']) # chap params should always have type
    if type=='sql':
        sql_example(listing_params)
    elif type=='py':
        python_example(listing_params)
    else:
        raise Exception('Unsupported type %s' % type)

