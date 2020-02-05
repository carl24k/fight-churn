from postgres import Postgres
import json
import pandas as pd
from importlib import import_module
from copy import copy
import re
import os
import sys
import argparse

'''
####################################################################################################
Arguments
'''
parser = argparse.ArgumentParser()
# Run control arguments
parser.add_argument("--schema", type=str, help="The name of the schema", default='socialnet7')
parser.add_argument("--chapter", type=int, help="The chapter of the listing", default=2)
parser.add_argument("--listing", nargs='*', type=int, help="The number of the listing", default=[1])
parser.add_argument("--insert", action="store_true", default=False,help="Use the insert version of a metric SQL, if available")
parser.add_argument("--version", nargs='*', help="Alternative listing _parameter_ verions (optional)",default=[])


'''
####################################################################################################
Constants
'''

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print_num_rows=10

reserved_param_keywords = ('listing', 'mode','type','schema','name','chapter')

'''
####################################################################################################
Functions
'''



def sql_listing(param_dict):
    '''
    Run a SQL listing.  The sql file is loaded, and then any non-reserved keyword in the parameters is treated as a
    string to be replaced in the sql string. The SQL is then printed out, before newlines are removed, and then run
    in one of the allowed modes.  The allowed modes are:
        run : The SQL returns no result
        one : The SQL should return one row result to be printed
        top : The SQL returns many results, print the top N (given by global print_num_rows)
    :param param_dict: dictionary produced by load_and_check_listing_params
    :return:
    '''


    with open('../../listings/chap%d/%s.sql' % (param_dict['chapter'], param_dict['name']), 'r') as myfile:
        db = Postgres("postgres://%s:%s@localhost/%s" % (os.environ['CHURN_DB_USER'],os.environ['CHURN_DB_PASS'],os.environ['CHURN_DB']))

        # prefix the search path onto the listing, which does not specify the schema
        sql = "set search_path = '%s'; " % param_dict['schema'];

        # load the sql file
        sql = sql + myfile.read()

        # bind any parameters that match strings in the sql
        param_keys = [p for p in param_dict.keys() if p not in reserved_param_keywords]
        for p in param_keys:
            sql = sql.replace(p, str(param_dict[p]))

        # Print the sql (then remove the newlines)
        print('SQL:\n----------\n'+sql+'\n----------\nRESULT:')
        sql = sql.replace('\n', ' ')

        # Run in the manner indicated by the mode
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
                csv_path= save_path + param_dict['schema'] + '_' +  param_dict['name'].replace(
                    'listing_{}_{}_'.format(param_dict['chapter'],param_dict['listing']),'')
                if 'save_ext' in param_dict:
                    csv_path = csv_path + '_' + param_dict['save_ext']
                csv_path = csv_path + '.csv'
                print('Saving: %s' % csv_path)
                df.to_csv(csv_path, index=False)
            else:
                print(df.head(print_num_rows))
        else:
            print('Unknown run mode for SQL example')
            exit(-4)


def python_listing(param_dict):
    '''
    Runs one python code listing.  Each listing is defined as a model, and should have one function in it, which is the name of
    the listing file, without the part saying listing_X_Y.  If the function is found in the module it is run; all of the
    non-reserved keywords in the parameter dictionary are treated as the parameters
    :param param_dict: dictionary produced by load_and_check_listing_params
    :return:
    '''

    # make a dictionary of just the non-reserved keywords, which should be the parameters
    example_params = {}
    for k in param_dict.keys():
        if k in reserved_param_keywords: continue
        example_params[k]=param_dict[k]

    # Load the listing name module
    mod = import_module(param_dict['name'])

    # Find the function name from the listing name
    example_name_regexp = 'listing_\\d+_\\d+_(\w+)'

    m = re.search(example_name_regexp, param_dict['name'])

    if m:
        ex_name = m.group(1)
        # Load the function, which is an attribute of the module
        ex_fun = getattr(mod, ex_name,None)
        if ex_fun is not None:
            # Run the function, passing the parameters
            ex_fun(**example_params)
        else:
            print('Could not find function %s in module %s' % (ex_name , param_dict['name']))
            exit(-5)
    else:
        print('Could not parse listing name %s in schema %s' % ( param_dict['name'], param_dict['schema']))
        exit(-6)


def load_and_check_listing_params(args):
    '''
    Loads the JSON of parameters for this schema, and gets the parameters for the specified listing. It raises errors if
    it cannot find what it is looking for. Once it finds the entry for this listing, it starts with the chapter default
    params, and then adds any parameters specific to the listing (which would override the chapter parameters, if there
    was one of the same name.) It also adds context information to the result, so that it has all the information needed
    when the listings are run.
    TODO: There is uncovered case in checking the params - it does not error on two entries matching the prefix
    :param schema: string name
    :param chapter: chapter number
    :param listing: listing number (or in some cases a letter)
    :return: dictionary of name value pairs for the example
    '''
    schema = args.schema
    chapter = args.chapter
    listing = args.listing
    version = args.version

    chapter_key='chap{}'.format(chapter)
    if not args.insert and version is None:
        listing_prefix='^listing_{c}_{l}_(?!\\d)'.format(c=chapter,l=listing)
    elif args.insert and version is None:
        listing_prefix='^insert_{c}_{l}_(?!\\d)'.format(c=chapter,l=listing)
    elif args.insert and version is not None:
        listing_prefix='^insert_{c}_{l}_{v}_'.format(c=chapter,l=listing,v=version)
    elif not args.insert and version is not None:
        listing_prefix='^listing_{c}_{l}_{v}_'.format(c=chapter,l=listing,v=version)

    listing_re=re.compile(listing_prefix)

    # Error if there is no file for this schema
    conf_path='../../listings/conf/%s_listings.json' % schema
    if not os.path.isfile(conf_path):
        print('No params %s to run listings on schema %s' % (conf_path,schema))
        exit(-1)

    with open(conf_path, 'r') as myfile:
        param_dict=json.loads(myfile.read())

    # Error if there is no key for this chapter in the dictionary
    if not chapter_key in param_dict:
        print('No params for chapter %d in %s_listings.json' % (chapter,schema))
        exit(-2)

    matches = list(filter(listing_re.match, param_dict[chapter_key].keys()))
    if len(matches)==0:
        print('No params for listing %d, chapter %d in %s_listings.json' % (listing, chapter, schema))
        exit(-3)

    if len(matches)>1:
        print('Multiple configurations found matching listing %d, chapter %d in %s_listings.json' % (listing, chapter, schema))
        exit(-4)

    listing_name = matches[0]
    # Start with the chapter default parameters
    listing_params = copy(param_dict[chapter_key]['params'])

    # If there are specific parameters for this listing, add them here
    if len(param_dict[chapter_key][listing_name])>0:
        for k in param_dict[chapter_key][listing_name].keys():
            listing_params[k]=param_dict[chapter_key][listing_name][k]

    # Add the other contextual information
    listing_params['schema'] = schema
    listing_params['chapter']=chapter
    listing_params['listing']=listing
    if args.version is None:
        listing_params['name'] = listing_name
        if listing_params['type']=='sql': listing_params['prefix'] = 'listing_{c}_{l}_'.format(c=chapter,l=listing)
    else:
        pre = 'listing' if not args.insert else 'insert'
        # For a versioned set of parameters, the listing file name must be the original...
        version_prefix='{p}_{c}_{l}_{v}_'.format(p=pre,c=chapter,l=listing,v=version)
        listing_prefix='{p}_{c}_{l}_'.format(p=pre,c=chapter,l=listing)
        listing_params['name'] = listing_name.replace(version_prefix,listing_prefix)
        if listing_params['type']=='sql': listing_params['prefix']=version_prefix

    if args.insert: # force the right mode forn insert sqls
        listing_params['mode']='run'

    return listing_params

    # Another error if it didn't find a listing



def run_one_listing(args):
    '''
    Load the dictionary of parameters for this schema
    Check the type of the listing (SQL or Python) and call the executor function
    :param schema: string
    :param chapter: number
    :param listing: number (or sometimes a string)
    :return:
    '''
    # Get arguments
    listing_params = load_and_check_listing_params(args)

    print('\nRunning %d listing %s on schema %s' % (args.chapter,listing_params['name'],args.schema))

    # Run the executor function for sql or for python...
    type = listing_params.get('type', listing_params['type']) # chap params should always have type
    if type=='sql':
        sql_listing(listing_params)
    elif type=='py':
        python_listing(listing_params)
    else:
        raise Exception('Unsupported type %s' % type)

'''
####################################################################################################
The main script for running Fight Churn With Data examples: If there are command line arguments, 
use them. Otherwise defaults are hard coded

'''

if __name__ == "__main__":
    args, _ = parser.parse_known_args()

    for l in args.listing:
        list_args = copy(args)
        list_args.listing = l
        if len(args.version)==0:
            list_args.version=None
            run_one_listing(list_args)
        else:
            for v in args.version:
                vers_args = copy(list_args)
                vers_args.version =v
                run_one_listing(vers_args)
