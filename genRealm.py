#!/bin/python

import json
import uuid
from pprint import pprint

realmDNSname='gawati.org'
realmDisplayName="Gawati"

UIDmap={'MODEL': realmDNSname}
UIDnames=['id', 'containerId']
DATAmap=[['MODEL',realmDNSname]]
realm = json.load(open('model_realm/model-realm.json'))


def swapIDs(data):
  if (isinstance(data, list)):
    for item in data:
      if (isinstance(item, (dict, list))):
        swapIDs(item)
    return

  for idType in UIDnames:
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


def applyDataMap(S):
  #print ('Apply data map from :'+S)
  for [pattern,value] in DATAmap:
    S=S.replace(pattern,value)
  #print ('to :'+S)
  return S


def updateURLs(X):
  if 'baseUrl' in X.keys():
    X['baseUrl']=applyDataMap(X['baseUrl'])

  if 'redirectUris' in X.keys():
    X['redirectUris']=list(map(applyDataMap,X['redirectUris']))


def whereXisYinS_mergeT(X,Y,S,T):
  for data in (filter(lambda item: item[X] == Y, S)):
    data.update(T)


def whereXisYinS_runF(X,Y,S,F):
  for data in (filter(lambda item: item[X] == Y, S)):
    F(data)


swapIDs(realm)

realm['realm']=realmDNSname
realm['displayName']=realmDisplayName
realm['displayNameHtml']=realmDisplayName

for client in ['security-admin-console','account']:
  whereXisYinS_runF('clientId',client,realm["clients"],updateURLs)

#print ('Applied map:')
#pprint (UIDmap)
print(json.dumps(realm, sort_keys=True, indent=4, separators=(',', ': ')))

