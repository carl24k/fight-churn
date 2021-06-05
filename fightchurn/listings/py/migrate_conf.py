import json
from collections import OrderedDict
import re

conf_path = '../../listings/conf/socialnet7_listings.json'

with open(conf_path, 'r') as myfile:
    param_dict = json.loads(myfile.read())

new_conf = OrderedDict()

for chap in param_dict.keys():
    new_conf[chap] = OrderedDict()
    for listing in param_dict[chap].keys():
        if listing=='params':
            new_conf[chap]['defaults']=param_dict[chap]['params']
            continue
        # print(listing)
        parts=listing.split('_')
        print(parts)
        list_type=parts[0]
        chap_num=parts[1]
        list_num=parts[2]
        if parts[3].isdigit():
            vers_num=parts[3]
            list_name='_'.join(parts[4:])
        else:
            vers_num = None
            list_name='_'.join(parts[3:])

        list_num_name = f'list{list_num}'
        if not list_num_name in new_conf[chap]:
            new_conf[chap][list_num_name] = OrderedDict()
            new_conf[chap][list_num_name]['name']=list_name

        if list_type == 'insert':
            if 'insert' not in new_conf[chap][list_num_name]:
                new_conf[chap][list_num_name]['insert']=OrderedDict()
            param_target = new_conf[chap][list_num_name]['insert']
        else:
            param_target = new_conf[chap][list_num_name]

        if vers_num:
            vers_num_name = f'v{vers_num}'
            param_target[vers_num_name] = param_dict[chap][listing]
            # if there are defaults, remove version params matching defaults
            if 'params' in param_target:
                for k in list(param_target[vers_num_name].keys()):
                    if k in param_target['params']:
                        if param_target[vers_num_name][k]==param_target['params'][k]:
                            param_target[vers_num_name].pop(k)
        else:
            param_target['params'] =param_dict[chap][listing]


save_path = '../../listings/conf/socialnet7_listings_v2.json'

with open(save_path, 'w') as myfile:
    json.dump(new_conf,myfile,indent=4)
