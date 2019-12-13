import os

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

        timestamp = jira_util.format_string_containing_iso_date(last_inserted_doc)
        data = poll_daily_jira_data(timestamp=timestamp)
        status_code_dict = handle_request_status(data)
        if status_code_dict is not None:
            return status_code_dict
        stripped_data = jira_util.strip_data(data.json())
        stripped_data.sort(key=lambda x: x['timestamp'])
        return post_jira_data(stripped_data)
    return create_status_code_dict(500)


def post_jira_data(data: list) -> dict:
    for issue in data:
        post_response = jira_util.handle_http_request(
            lambda: jira_util.post_to_ingest(
                url=INGEST_URL,
                api_key=INGEST_API_KEY,
                data=issue
            )
        )
        if post_response.status_code != 200:
            return create_status_code_dict(post_response.status_code)

    jira_util.upload_last_inserted_doc(timestamp=data[-1]['timestamp'], data_type=JIRA_SALES_TYPE)
    return create_status_code_dict(post_response.status_code)


def handle_request_status(data: object) -> dict:
    if data.status_code != 200:
        return create_status_code_dict(data.status_code)
    if len(data.json()['issues']) < 1:
        return create_status_code_dict(61)
    return None


def poll_daily_jira_data(timestamp: str) -> object:
    jql = f'project=SALG and created > {timestamp}'
    get_response = jira_util.handle_http_request(
        lambda: jira_util.get_sales_data_from_jira(
            url=JIRA_URL,
            username=JIRA_USERNAME,
            password=JIRA_PASSWORD,
            params=jira_util.create_params_dict(jql=jql)
        )
    )
    return get_response


def create_status_code_dict(code: int) -> dict:
    return {
        'status_code': code,
        'body': ''
    }
