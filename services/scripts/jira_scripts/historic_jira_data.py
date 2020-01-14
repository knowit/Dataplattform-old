import itertools
import os
from dotenv import load_dotenv

from services.poller.jira_poller import jira_util
import historic_jira_data_util


def main():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))
    JIRA_SALES_TYPE = "JiraSalesType"
    if os.getenv("DATAPLATTFORM_INGEST_URL"):
        INGEST_URL = os.getenv("DATAPLATTFORM_INGEST_URL") + JIRA_SALES_TYPE
    INGEST_API_KEY = os.getenv("DATAPLATTFORM_INGEST_APIKEY")

    data = historic_jira_data_util.get_jira_data()
    flattened_data = list(itertools.chain.from_iterable(data))
    flattened_data.sort(key=lambda x: x['updated'])

    historic_jira_data_util.post_to_ingest_loop(data=flattened_data, ingest_url=INGEST_URL,
                                                ingest_api_key=INGEST_API_KEY)

    response = jira_util.publish_event_to_sns(flattened_data)
    print("////////////////////////////////RESPONSE//////////////////////////////")
    print(response)

    jira_util.upload_last_inserted_doc(timestamp=flattened_data[-1]['updated'], data_type=JIRA_SALES_TYPE)


main()
