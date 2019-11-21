import os
import json
import urllib.request
import requests
from datetime import datetime


AD_TYPE = 'ADType'

non_humans = [
    'anbud on',
    'creative crew',
    'innovation tuesday',
    'info tavle',
    'oslo event',
    'vegloggen bruker'
]


def handler(event, context):

    record = poll()
    code = post_to_ingest(record)

    return {
        'statusCode': code,
        'body': ''
    }


def post_to_ingest(data):
    ingest_url = os.getenv("DATAPLATTFORM_INGEST_URL") + AD_TYPE
    apikey = os.getenv("DATAPLATTFORM_INGEST_APIKEY")

    data = json.dumps(data).encode()
    try:
        request = urllib.request.Request(ingest_url, data=data, headers={"x-api-key": apikey})
        response = urllib.request.urlopen(request)
        return response.getcode()
    except urllib.request.HTTPError:
        return 500


def poll():
    r = requests.get(url=os.getenv("DATAPLATTFORM_AD_URL"))
    data = r.json()

    retrieved = datetime.now().timestamp()

    emps, dis_emps, conts, dis_conts = count_emps(data)

    record = {'retrieved': retrieved, 'count_employees': emps, 'count_discontinued_employees': dis_emps,
              'count_subcontractors': conts, 'count_discontinued_subcontractors': dis_conts,
              'count_all': emps + conts, 'count_discontinued_all': dis_emps + dis_conts}

    return record


def count_emps(data):
    email_users = {}

    emps = 0
    dis_emps = 0
    conts = 0
    dis_conts = 0

    for a in data:

        if a['userDetails']['isServiceUser']:
            continue
        if a['userDetails']['displayName'].lower() in non_humans:
            continue

        email = a['userDetails']['userPrinicipalName']
        if email not in email_users:
            email_users[email] = a
        else:
            continue

        if a['userDetails']['isExternalUser']:
            if (a['userDetails']['isDeleted']):
                dis_conts += 1
            else:
                conts += 1
        else:
            if (a['userDetails']['isDeleted']):
                dis_emps += 1
            else:
                emps += 1

    return emps, dis_emps, conts, dis_conts










