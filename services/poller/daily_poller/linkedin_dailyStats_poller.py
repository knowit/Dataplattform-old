import os
import json
import requests_oauthlib
from datetime import datetime, timedelta
from poller_util import PollerUtil

LINKEDIN_ORGS = {
    "knowit ab": "urn:li:organization:8067",
    "knowit solutions": "urn:li:organization:15179956",
}

LINKEDIN_DAILY_FOLLOWER_STATS_TYPE = "LinkedInDailyFollowerStatsType"
LINKEDIN_DAILY_PAGE_STATS_TYPE = "LinkedInDailyPageStatsType"
LINKEDIN_DAILY_SHARE_STATS_TYPE = "LinkedInDailyShareStatsType"


LINKEDIN_APIS = {
    LINKEDIN_DAILY_FOLLOWER_STATS_TYPE: "https://api.linkedin.com/v2/organizationalEntityFollowerStatistics?"
                                "q=organizationalEntity&organizationalEntity=PLACEHOLDER_ORG"
                                "&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start="
                                "PLACEHOLDER_START&timeIntervals.timeRange.end=PLACEHOLDER_END",

    LINKEDIN_DAILY_PAGE_STATS_TYPE: "https://api.linkedin.com/v2/organizationPageStatistics?q=organization&organization="
                            "PLACEHOLDER_ORG&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start=" 
                            "PLACEHOLDER_START&timeIntervals.timeRange.end=PLACEHOLDER_END",

    LINKEDIN_DAILY_SHARE_STATS_TYPE: "https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity"
                             "&organizationalEntity=PLACEHOLDER_ORG&timeIntervals.timeGranularityType=DAY&"
                             "timeIntervals.timeRange.start=PLACEHOLDER_START&timeIntervals.timeRange.end=PLACEHOLDER_END"
}


def authenticate():

    client_id = os.getenv("DATAPLATTFORM_LINKEDIN_CLIENT_ID")
    token = os.getenv("DATAPLATTFORM_LINKEDIN_TOKEN")
    token = json.loads(token)

    try:
        client = requests_oauthlib.OAuth2Session(client_id=client_id, token=token)
    except:
        client = None

    return client


def poll():
    client = authenticate()

    for org_name in LINKEDIN_ORGS.keys():
        for api_type in LINKEDIN_APIS.keys():
            doc_name = api_type+org_name.replace(" ", "").upper()

            last_inserted_timestamp = 0
            last_inserted_doc = PollerUtil.fetch_last_inserted_doc(doc_name)
            if last_inserted_doc:
                last_inserted_timestamp = int(last_inserted_doc)

            data_points = poll_daily_stats_data(client, LINKEDIN_ORGS[org_name],
                                                org_name, LINKEDIN_APIS[api_type],
                                                last_inserted_timestamp)
            if not data_points:
                continue

            for data_point in data_points:
                result = PollerUtil.post_to_ingest_api(data_point, api_type)
                if result is not None:
                    last_inserted_timestamp = data_point['data']['timeRange']['end']

            PollerUtil.upload_last_inserted_doc(last_inserted_timestamp, doc_name)

    return True


def poll_daily_stats_data(client, organization_id, organization_name, api, last_inserted_timestamp):
    data_points = []
    curr_time = datetime.now()
    if last_inserted_timestamp == 0:
        last_inserted_timestamp = (curr_time - timedelta(days=365)).timestamp()

    query = build_query(api, organization_id, curr_time.timestamp(), last_inserted_timestamp)

    response = client.get(query)
    if response.status_code != 200:
        return None

    data = json.loads(response.content)

    for elem in data['elements']:
        record = {'page': organization_name, 'data': elem}
        data_points.append(record)

    return data_points


def fix_timestamp(timestamp):
    while len(timestamp) < 13:
        timestamp += "0"
    return timestamp


def build_query(api, organization_id, curr_timestamp, last_inserted_timestamp):
    curr_timestamp = fix_timestamp(str(int(curr_timestamp)))
    yesterday_timestamp = fix_timestamp(str(int(last_inserted_timestamp)))
    query = api.replace("PLACEHOLDER_ORG", organization_id)
    query = query.replace("PLACEHOLDER_START", yesterday_timestamp)
    query = query.replace("PLACEHOLDER_END", curr_timestamp)
    return query
