import sys
from typing import Callable
import json
import dateutil.parser
import requests
from requests.exceptions import HTTPError
import boto3
import os

from poller_util import PollerUtil


def encapsule_data_with_json(data: list) -> str:
    dictionary = {
        'default': "Publish jira events",
        'data': data
    }
    return json.dumps(dictionary)


def publish_event_to_sns(data: list) -> int:
    sns = boto3.client('sns')

    response = sns.publish(
        TopicArn=os.getenv("DATAPLATTFORM_PUBLISH_JIRA"),
        Message=encapsule_data_with_json(data),
    )

    return response['ResponseMetadata']['HTTPStatusCode']


def handle_http_request(request_function: Callable) -> object:
    try:
        response = request_function()
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return response
    else:
        return response


def create_params_dict(
        jql: str = "project=SALG and status != 'Rejected'",
        start_at: int = 0,
        max_results: int = 500
) -> dict:
    return {
        'jql': jql,
        'fields': 'labels, status, created, updated',
        'maxResults': max_results,
        'startAt': start_at
    }


def strip_data(data: list) -> list:
    stripped = []
    for item in data['issues']:
        customer = ''
        if len(item['fields']['labels']) > 0:
            customer = item['fields']['labels'][0]
        issue = {
            'issue': item['key'],
            'customer': customer,
            'status': item['fields']['status']['name'],
            'created': item['fields']['created'],
            'updated': item['fields']['updated']
        }
        stripped.append(issue)
    return stripped


def post_to_ingest(url: str, api_key: str, data: dict) -> object:
    encoded_data = json.dumps(data).encode()
    response = requests.post(url=url, data=encoded_data, headers={'x-api-key': api_key})
    return response


def format_string_containing_iso_date(iso_date_string: str) -> str:
    iso_date = dateutil.parser.parse(iso_date_string)
    return iso_date.strftime("'%Y/%m/%d'")


def upload_last_inserted_doc(timestamp: str, data_type: str):
    last_inserted_doc = format_string_containing_iso_date(iso_date_string=timestamp)
    PollerUtil.upload_last_inserted_doc(
        last_inserted_doc=last_inserted_doc,
        type=data_type
    )
