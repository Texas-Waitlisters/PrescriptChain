import requests
import base64
import datetime
import json
apikey = 'GUWiB4x3JwrOiaWyFMYLlRmfJr7YfFFGDMzwYG80sdtL4BDT'

def version(key):
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/'
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    r = requests.get(url, headers=headers)
    return r;

def createChain(key,externalID,content):
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/chains'
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    data = {'external_ids':[BASE64(externalID),BASE64(unixTime())],'content':BASE64(content) }
    print(BASE64("externalID"))
    r = requests.post(url, json=data, headers=headers)
    return r;

def getAllChains(key):
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/chains'
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    r = requests.get(url, headers=headers)
    return r;

def searchChains(key,searchList):
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/chains'
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    list = [BASE64(element) for element in searchList]
    data = {'external_ids':list}
    r = requests.post(url, json=data, headers=headers)
    return r;

def getChainInfo(key,chainID):
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/chains/'+chainID
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    r = requests.get(url, headers=headers)
    return r;

def createEntry(key,chainID,externalID,content):
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/chains/'+chainID+'/entries'
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    data = {'external_ids':[BASE64(externalID),BASE64(unixTime())],'content':BASE64(content) }
    r = requests.post(url, json=data, headers=headers)
    return r;

def getAllEntries(key,chainID):
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/chains/'+chainID+'/entries'
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    r = requests.get(url, headers=headers)
    return r;

def searchEntries(key,chainID,searchList):
    list = [BASE64(element) for element in searchList]
    url = 'https://apiplus-api-sandbox-testnet.factom.com/v1/chains/'+chainID+'/entries/search'
    headers = {'Content-Type': 'application/json', 'factom-provider-token': key }
    data = {'external_ids':list }
    r = requests.post(url, json=data, headers=headers)
    return r;


def BASE64(str):
    return base64.b64encode(str.encode('utf-8')).decode('utf-8')

def unixTime():
    return '{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())

req = version(apikey)
req = getAllEntries(apikey, "b94bdc176602f8445eae74a684ae31f4dfee821334f127905d67a06b6b41b7ed")
print(req.text)
print(req)
print(req.json)
req = searchEntries(apikey, "b94bdc176602f8445eae74a684ae31f4dfee821334f127905d67a06b6b41b7ed", ["12893677bf5f96d17256262be44a17f576c1c9782586f59f636d34a220b14b5e","439ee0d1e9aa8529c42fca3553e3d2ccbbf0059067fa94a1f1694fff17cf03dc"])
print(req.text)
print(req)
print(req.json)
