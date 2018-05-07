#!/bin/python

import json
import uuid
from pprint import pprint

debug=False

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
        DATAmap.append([data[idType],UIDmap[data[idType]]])
      if debug: print ('old ' + idType + ' : ' + str(data[idType]))
      if debug: print ('new ' + idType + ' : ' + str(UIDmap[data[idType]]))
      data[idType] = UIDmap[data[idType]]

  for item in data:
    if (isinstance(data[item], (dict, list))):
      if debug: print ('Container: ' + item)
      swapIDs(data[item])


def applyDataMap(S):
  if debug: print ('Apply data map from :'+S)
  for [pattern,value] in DATAmap:
    S=S.replace(pattern,value)
  if debug: print ('to :'+S)
  return S


def updateURLs(X):
  if debug: print ('updateURLs')
  if 'baseUrl' in X.keys():
    X['baseUrl']=applyDataMap(X['baseUrl'])
  if 'redirectUris' in X.keys():
    X['redirectUris']=list(map(applyDataMap,X['redirectUris']))


def whereXisYinS_mergeT(X,Y,S,T):
  if debug: print('whereXisYinS_mergeT')
  for data in (filter(lambda item: item[X] == Y, S)):
    data.update(T)


def whereXisYinS_runF(X,Y,S,F):
  if debug: print('whereXisYinS_runF')
  for data in (filter(lambda item: item[X] == Y, S)):
    F(data)


def whereXexistsinS_runF(X,S,F):
  if debug: print ('whereXexistsinS_runF: >'+X+'<')
  if X in S.keys():
    F(S[X])


def updatePolicies(S):
  if debug: print ('updatePolicies')
  for policy in S:
    if 'name' in policy.keys():
      policy['name']=applyDataMap(policy['name'])
    if 'config' in policy.keys():
      if 'resources' in policy['config'].keys():
        policy['config']['resources']=applyDataMap(policy['config']['resources'])


def updateAuth(S):
  if debug: print ('updateAuth')
  whereXexistsinS_runF('policies',S,updatePolicies)
  whereXexistsinS_runF('resources',S,updatePolicies)
    

swapIDs(realm)

realm['realm']=realmDNSname
realm['displayName']=realmDisplayName
realm['displayNameHtml']=realmDisplayName
realm['attributes']['displayName']=realmDisplayName
realm['attributes']['displayNameHtml']=realmDisplayName

for client in ['security-admin-console','account']:
  whereXisYinS_runF('clientId',client,realm["clients"],updateURLs)

if debug: print('auths')
for client in realm["clients"]:
  whereXexistsinS_runF('authorizationSettings',client,updateAuth)

if debug: print ('Applied map:')
if debug: pprint (UIDmap)
print(json.dumps(realm, sort_keys=True, indent=4, separators=(',', ': ')))

