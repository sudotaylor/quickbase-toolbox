#!/usr/bin/env python3
# quickbaseBulkDownloadFiles.py
# Download previously uploaded files from Quickbase in bulk 

import json
import requests
import base64
import urllib.parse as urlParse

# constants -- YOU NEED TO FILL THESE IN! :D
realmHostname = '' # use the full hostname -- e.g. 'your-realm.quickbase.com'
token = '' # you'll need a user token for the API calls
table = '' # table ID -- you can obtain this from the URL when visiting the page of the table
field = 0 # integer corresponding to the field ID containing the files
keyField = 3 # the key field ID -- the default is 3
conditions = '' # this is how you select which records to pull from -- use formula query format described in QB API documentation

headers = {
    'QB-Realm-Hostname': realmHostname,
    'User-Agent': '{User-Agent}',
    'Authorization': 'QB-USER-TOKEN ' + token
}

def LocateRecords():
    # Basically SQL:
    #   SELECT [FIELD(S)] FROM [TABLE] WHERE [CONDITION(S)]
    query = {
        "select": [str(keyField)],
        "from": table,
        "where": conditions
    }
    response = requests.post('https://api.quickbase.com/v1/records/query', headers = headers, json = query)
    data = response.json()
    recs = []
    for datum in data['data']:
        recs.append(datum[str(keyField)]['value'])
    FetchRecords(recs)

def FetchRecords(recs):
    for rec in recs:
        response = requests.get('https://api.quickbase.com/v1/files/' + table + '/' + str(rec) + '/' + str(field) + '/1', headers = headers) # file version 1
        # Enable if you want some feedback on the request statuses:
        #print("Status Code: " + str(response.status_code))
        filename = urlParse.unquote(response.headers['content-disposition'][29:])
        with open(filename, "wb") as fh:
            fh.write(base64.decodebytes(response.content))
        fh.close

LocateRecords()
