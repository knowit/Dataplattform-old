import os
import requests

import jira_util
from poller_util import PollerUtil

JIRA_URL = os.getenv("DATAPLATTFORM_JIRA_SALES_URL")
JIRA_USERNAME = os.getenv("DATAPLATTFORM_JIRA_SALES_USERNAME")
JIRA_PASSWORD = os.getenv("DATAPLATTFORM_JIRA_SALES_PASSWORD")

JIRA_SALES_TYPE = "JiraSalesType"
if os.getenv("DATAPLATTFORM_INGEST_URL"):
    INGEST_URL = os.getenv("DATAPLATTFORM_INGEST_URL") + JIRA_SALES_TYPE
INGEST_API_KEY = os.getenv("DATAPLATTFORM_INGEST_APIKEY")


def handler(event, context) -> dict:
    last_inserted_doc = PollerUtil.fetch_last_inserted_doc(type=JIRA_SALES_TYPE)
    if last_inserted_doc:
        data = get_jira_data(
            timestamp=jira_util.format_string_containing_iso_date(last_inserted_doc)
        )
        status_code_dict = handle_request_status(data)
        if status_code_dict is not None:
            return status_code_dict

        stripped_data = jira_util.strip_data(data.json())
        stripped_data.sort(key=lambda x: x['updated'])

        ingest_response_status_code = post_jira_data_to_ingest(stripped_data)
        sns_response_status_code = jira_util.publish_event_to_sns(stripped_data)
        jira_util.upload_last_inserted_doc(
            timestamp=stripped_data[-1]['updated'],
            data_type=JIRA_SALES_TYPE
        )
        if ingest_response_status_code == 200 and sns_response_status_code == 200:
            return create_status_code_dict(code=200)
    return create_status_code_dict(code=500)


def post_jira_data_to_ingest(data: list) -> int:
    for issue in data:
        post_response = jira_util.handle_http_request(
            lambda: jira_util.post_to_ingest(
                url=INGEST_URL,
                api_key=INGEST_API_KEY,
                data=issue
            )
        )
        if post_response.status_code != 200:
            return post_response.status_code
    return post_response.status_code


def handle_request_status(data: object) -> dict:
    if data.status_code != 200:
        return create_status_code_dict(data.status_code)
    if len(data.json()['issues']) < 1:
        return create_status_code_dict(code=61)
    return None


def get_jira_data(timestamp: str) -> object:
    jql = f"project=SALG and status != 'Rejected' and updated > {timestamp}"
    get_response = jira_util.handle_http_request(
        lambda: requests.get(
            url=JIRA_URL,
            params=jira_util.create_params_dict(jql=jql),
            auth=(JIRA_USERNAME, JIRA_PASSWORD)
        )
    )
    return get_response


def create_status_code_dict(code: int) -> dict:
    return {
        'status_code': code,
        'body': ''
    }
