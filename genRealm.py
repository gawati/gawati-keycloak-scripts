#!/bin/python

import json
import uuid
from pprint import pprint

UIDmap={u'MODEL': u'gawati.org'}
idTypes=['id', 'containerId']
realm = json.load(open('model_realm/model-realm.json'))

def swapIDs(data):
  if (isinstance(data, list)):
    for item in data:
      if (isinstance(item, (dict, list))):
        swapIDs(item)
    return

  for idType in idTypes:
    if (idType in data.keys()):
      if not(data[idType] in UIDmap.keys()):
        UIDmap[data[idType]] = str(uuid.uuid4())
      #print ('old ' + idType + ' : ' + str(data[idType]))
      #print ('new ' + idType + ' : ' + str(UIDmap[data[idType]]))
      data[idType] = UIDmap[data[idType]]

  for item in data:
    if (isinstance(data[item], (dict, list))):
      #print ('Container: ' + item)
      swapIDs(data[item])

swapIDs(realm) 
#print ('Applied map:')
#pprint (UIDmap)
print(json.dumps(realm, sort_keys=True, indent=4, separators=(',', ': ')))

