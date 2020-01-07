import sys
from typing import Callable
import json
import dateutil.parser
import requests
from requests.exceptions import HTTPError

from poller_util import PollerUtil


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
    return {'jql': jql, 'fields': 'labels, status, created, updated',
            'maxResults': max_results, 'startAt': start_at}


def get_sales_data_from_jira(
        url: str,
        username: str,
        password: str,
        params: dict
) -> object:
    response = requests.get(url=url, params=params, auth=(username, password))
    return response


def strip_data(data: list) -> list:
    stripped = []
    for item in data['issues']:
        customer = ''
        if len(item['fields']['labels']) > 0:
            customer = item['fields']['labels'][0]
        issue = {'timestamp': item['fields']['created'],
                 'customer': customer,
                 'status': item['fields']['status']['name'],
                 'issue': item['key']}
        stripped.append(issue)
    return stripped


def post_to_ingest(url: str, api_key: str, data: dict) -> object:
    encoded_data = json.dumps(data).encode()
    response = requests.post(url=url, data=encoded_data, headers={'x-api-key': api_key})
    return response


def post_to_ingest_loop(data: list, ingest_url: str, ingest_api_key: str):
    for i, issue in enumerate(data):
        print('issue:', i)
        post_response = handle_http_request(
            request_function=lambda: post_to_ingest(
                url=ingest_url,
                api_key=ingest_api_key,
                data=issue
            )
        )
    if post_response.status_code != 200:
        sys.exit()


def format_string_containing_iso_date(iso_date_string: str) -> str:
    iso_date = dateutil.parser.parse(iso_date_string)
    return iso_date.strftime("'%Y/%m/%d'")


def upload_last_inserted_doc(timestamp: str, data_type: str):
    last_inserted_doc = format_string_containing_iso_date(iso_date_string=timestamp)
    PollerUtil.upload_last_inserted_doc(
        last_inserted_doc=last_inserted_doc,
        type=data_type
    )
