from postgres import Postgres
import json
import pandas as pd
from importlib import import_module
import re
import os

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
one_example=None
one_chapter=None



example_name_regexp='listing_\\d+_\\d+_(\w+)'

print_num_rows=5
flat_metric_bind = 'FLAT_METRIC_SELECT'
flat_metric_template = ', sum(case when metric_name_id=%d then metric_value else 0 end) as %s'

def generate_flat_metric_sql(db):
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
        elif mode == 'all' or mode == 'save':
            res = db.all(sql)
            df = pd.DataFrame(res)
            if mode == 'save':
                print('Saving...')
                df.to_csv(save_path + example + ' .csv', index=False)
            else:
                print(df.head(print_num_rows))

def python_example(param_dict,chapter,example):

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
    save_path = '../../../fight-churn-output/' + schema + '/'
    os.makedirs(save_path,exist_ok=True)

    chapter = 2
    listing = 1
    chapter_key='chap%d' % chapter
    listing_prefix='listing_%d_%d_' % (chapter,listing )

    with open('../conf/%s_examples.json' % schema, 'r') as myfile:
        param_dict=json.loads(myfile.read())

    if not chapter_key in param_dict:
        print('No params for chapter %d in %s_examples.json' % (chapter,schema))
        exit(-1)


    for example in param_dict[chapter_key].keys():

        if example=='params' or not listing_prefix in example:
            continue

        print('\nRunning %s listing %s' % (chapter_key,example))

        type = param_dict[chapter_key][example].get('type', param_dict[chapter_key]['params']['type']) # chap params should always have type
        if type=='sql':
            sql_example(param_dict,chapter_key,example)
        elif type=='py':
            python_example(param_dict,chapter_key,example)
        else:
            raise Exception('Unsupported type %s' % type)
