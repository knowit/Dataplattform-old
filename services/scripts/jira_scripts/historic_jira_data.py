import sys
import itertools
import os

from services.poller.jira_poller import jira_util
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))

JIRA_URL = os.getenv("DATAPLATTFORM_JIRA_SALES_URL")
JIRA_USERNAME = os.getenv("DATAPLATTFORM_JIRA_SALES_USERNAME")
JIRA_PASSWORD = os.getenv("DATAPLATTFORM_JIRA_SALES_PASSWORD")

JIRA_SALES_TYPE = "JiraSalesType"
if os.getenv("DATAPLATTFORM_INGEST_URL"):
    INGEST_URL = os.getenv("DATAPLATTFORM_INGEST_URL") + JIRA_SALES_TYPE
INGEST_API_KEY = os.getenv("DATAPLATTFORM_INGEST_APIKEY")


def get_jira_data() -> object:
    data = []
    max_results = 500
    max_total_number_of_jira_issues = 10000  # remember to update range if total number of issues from jira exceeds this (check request in postman)
    for i in range(0, max_total_number_of_jira_issues, max_results):

        get_response = jira_util.handle_http_request(
            lambda: jira_util.get_sales_data_from_jira(
                url=JIRA_URL,
                username=JIRA_USERNAME,
                password=JIRA_PASSWORD,
                params=jira_util.create_params_dict(start_at=i, max_results=max_results)
            )
        )
        if get_response.status_code != 200:
            sys.exit()
        else:
            stripped_data = jira_util.strip_data(get_response.json())
            if len(stripped_data) > 0:
                data.append(stripped_data)
    return data


def main():
    data = get_jira_data()
    flattened_data = list(itertools.chain.from_iterable(data))
    flattened_data.sort(key=lambda x: x['timestamp'])

    jira_util.post_to_ingest_loop(data=flattened_data, ingest_url=INGEST_URL, ingest_api_key=INGEST_API_KEY)
    jira_util.upload_last_inserted_doc(timestamp=flattened_data[-1]['timestamp'], data_type=JIRA_SALES_TYPE)

# main()
