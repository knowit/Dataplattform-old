import os
import requests
import sys
from services.poller.jira_poller import jira_util


def post_to_ingest_loop(data: list, ingest_url: str, ingest_api_key: str):
    for i, issue in enumerate(data):
        print('issue:', i)
        post_response = jira_util.handle_http_request(
            request_function=lambda: jira_util.post_to_ingest(
                url=ingest_url,
                api_key=ingest_api_key,
                data=issue
            )
        )
    if post_response.status_code != 200:
        print(post_response.status_code)
        sys.exit()


def get_jira_data() -> object:
    JIRA_URL = os.getenv("DATAPLATTFORM_JIRA_SALES_URL")
    JIRA_USERNAME = os.getenv("DATAPLATTFORM_JIRA_SALES_USERNAME")
    JIRA_PASSWORD = os.getenv("DATAPLATTFORM_JIRA_SALES_PASSWORD")
    data = []
    max_results = 500
    max_total_number_of_jira_issues = 10000  # remember to update range if total number of issues from jira exceeds this (check request in postman)
    for i in range(0, max_total_number_of_jira_issues, max_results):

        get_response = jira_util.handle_http_request(
            lambda: requests.get(
                url=JIRA_URL,
                params=jira_util.create_params_dict(start_at=i, max_results=max_results),
                auth=(JIRA_USERNAME, JIRA_PASSWORD)
            )
        )
        if get_response.status_code != 200:
            sys.exit()
        else:
            stripped_data = jira_util.strip_data(get_response.json())
            if len(stripped_data) > 0:
                data.append(stripped_data)
    return data
