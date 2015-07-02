#!/usr/bin/env python

import jinja2
import json
import yaml
import argparse
import copy
import os

hostAction = False

parser = argparse.ArgumentParser(
    description='Ansible inventory from jinja2 template')
parser.add_argument('--list', dest='listAction', action='store_true',
                    help='list all host groups')
parser.add_argument('--host', dest='hostAction', action='store',
                    help='list a particular host')

args = parser.parse_args()

templateLoader = jinja2.FileSystemLoader(
    searchpath=os.path.dirname(os.path.realpath(__file__)))
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "inventory_template.ini"
template = templateEnv.get_template(TEMPLATE_FILE)

# render template
outputText = template.render(env=os.environ)

# parse JSON
inventoryData = yaml.load(outputText)

listData = copy.deepcopy(inventoryData)
hostData = {}

for group in listData:
    # the JSON for --list is a shallower copy of the full
    # inventory JSON
    listData[group]['hosts'] = inventoryData[group]['hosts'].keys()
    # the _meta hostvars (which is also the basis for --host output)
    # is a concatenation of assigned hostvars
    for host in inventoryData[group]['hosts']:
        if host not in hostData:
            hostData[host] = {}
        for k in inventoryData[group]['hosts'][host]:
            hostData[host][k] = inventoryData[group]['hosts'][host][k]

listData['_meta'] = {}
listData['_meta']['hostvars'] = copy.deepcopy(hostData)

if args.hostAction:
    print json.dumps(hostData[args.hostAction],
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))
else:
    print json.dumps(listData,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))
