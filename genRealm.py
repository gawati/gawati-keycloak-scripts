#!/bin/python

import json
import uuid
import optparse
from pprint import pprint


optp = optparse.OptionParser()
optp.add_option('-d', '--debug', dest='debug', help='print debug messages', action='store_true', default=False)
optp.add_option('-r', '--realm', dest='realm', help='realm ID (DNS domain name recommended)', default='dev.gawati.org')
optp.add_option('-n', '--name', dest='name', help='verbose realm name (as reference name)', default='Gawati')
opts, args = optp.parse_args()

debug=opts.debug
realmDNSname=opts.realm
realmDisplayName=opts.name
clientURL='edit.'+realmDNSname
portalURL=realmDNSname

UIDmap={'MODEL': realmDNSname}
UIDnames=['id', 'containerId']
DATAmap=[['MODEL',realmDNSname],['client.rooturl',clientURL],['client.baseurl',clientURL],['client.adminurl',clientURL],['client.redirecturl',clientURL],['portal.rooturl',portalURL],['portal.baseurl',portalURL],['portal.adminurl',portalURL],['portal.redirecturl',portalURL]]
realm = json.load(open('model_realm/model-realm.json'))
MapClients=['security-admin-console','account','gawati-client','gawati-portal-ui']
MapFields=['baseUrl','redirectUris','rootUrl','adminUrl','baseUrl']


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
  if debug: print ('Apply data map from >' + S + '<')
  for [pattern,value] in DATAmap:
    S=S.replace(pattern,value)
  if debug: print ('to >' + S + '<')
  return S


def mapIfPresent(X,S):
  if debug: print ('mapIfPresent >' + X + '<')

  if X in S.keys():
    if debug: print ('  is present: mapping')
    if (isinstance(S[X], (list))):
      for i in range(len(S[X])):
        S[X][i]=applyDataMap(S[X][i])
    else:
      S[X]=applyDataMap(S[X])

  else:
    if debug: print ('  not present: mapping')


def mapFields(X):
  if debug: print ('mapFields')
  for item in MapFields:
    mapIfPresent(item,X)


def whereXisYinS_mergeT(X,Y,S,T):
  if debug: print('whereXisYinS_mergeT >' + X + '< is >' + Y + '<')
  for data in (filter(lambda item: item[X] == Y, S)):
    data.update(T)


def whereXisYinS_runF(X,Y,S,F):
  if debug: print('whereXisYinS_runF >' + X + '< is >' + Y + '<')
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

for client in MapClients:
  whereXisYinS_runF('clientId',client,realm["clients"],mapFields)

if debug: print('auths')
for client in realm["clients"]:
  whereXexistsinS_runF('authorizationSettings',client,updateAuth)

if debug: print ('Applied map:')
if debug: pprint (UIDmap)
print(json.dumps(realm, sort_keys=True, indent=4, separators=(',', ': ')))

