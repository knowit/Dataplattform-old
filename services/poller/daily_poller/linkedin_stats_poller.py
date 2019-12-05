import os
import json
import requests_oauthlib
from datetime import datetime
from poller_util import PollerUtil

SCOPE = ['rw_organization_admin',
         'r_organization_social']

LINKEDIN_ORGS = {
    "knowit ab": "urn:li:organization:8067",
    "knowit solutions": "urn:li:organization:15179956",
}

LINKEDIN_APIS = {
    "FOLLOWER_STATS_API": "https://api.linkedin.com/v2/organizationalEntityFollowerStatistics?"
                          "q=organizationalEntity&organizationalEntity=",
    "PAGE_STATS_API": "https://api.linkedin.com/v2/organizationPageStatistics?"
                      "q=organization&organization=",
    "SHARE_STATS_API": "https://api.linkedin.com/v2/organizationalEntityShareStatistics?"
                       "q=organizationalEntity&organizationalEntity="
}

DATA_TYPES = {
    "pageStatisticsBySeniority": "LinkedInPageStatisticsBySeniorityType",
    "pageStatisticsByCountry": "LinkedInPageStatisticsByCountryType",
    "pageStatisticsByIndustry": "LinkedInPageStatisticsByIndustryType",
    "pageStatisticsByStaffCountRange": "LinkedInPageStatisticsByStaffCountRangeType",
    "pageStatisticsByRegion": "LinkedInPageStatisticsByRegionType",
    "pageStatisticsByFunction": "LinkedInPageStatisticsByFunctionType",
    "totalPageStatistics": "LinkedInPageStatisticsTotalType",
    "followerCountsByAssociationType": "LinkedInFollowerCountsByAssociationType",
    "followerCountsByRegion": "LinkedInFollowerCountsByRegionType",
    "followerCountsBySeniority": "LinkedInFollowerCountsBySeniorityType",
    "followerCountsByIndustry": "LinkedInFollowerCountsByIndustryType",
    "followerCountsByStaffCountRange": "LinkedInFollowerCountsByStaffCountRangeType",
    "followerCountsByFunction": "LinkedInFollowerCountsByFunctionType",
    "followerCountsByCountry": "LinkedInFollowerCountsByCountryType",
    "totalShareStatistics": "LinkedInTotalShareStatisticsType"
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

    for key in LINKEDIN_ORGS.keys():
        data_points = poll_stats_data(client, LINKEDIN_ORGS[key], key)

        for data_point in data_points:
            for data_point_key in data_point.keys():
                PollerUtil.post_to_ingest_api(data_point[data_point_key], data_point_key)


def poll_stats_data(client, organization_id, organization_name):
    data_points = []

    for api in LINKEDIN_APIS.keys():
        query = LINKEDIN_APIS[api]+organization_id
        response = client.get(query)
        data = json.loads(response.content)
        time_fetched = datetime.now().strftime("%Y-%m-%d")
        data_points = filter_stats_data(api, data, organization_name, time_fetched, data_points)

    return data_points


def filter_stats_data(api, data, organization_name, time_fetched, data_points):

    for element in data['elements']:
        for key in element:
            if key not in DATA_TYPES.keys():
                continue
            if api == "FOLLOWER_STATS_API":
                data_points.append(follower_statistics_filter(element[key], key, organization_name, time_fetched))
            elif api == "PAGE_STATS_API":
                data_points.append(page_statistics_filter(element[key], key, organization_name, time_fetched))
            elif api == "SHARE_STATS_API":
                data_points.append(share_statistics_filter(element[key], key, organization_name, time_fetched))

    return data_points


def follower_statistics_filter(data, key, page, time):
    data_type = DATA_TYPES[key]
    data_string = json.dumps(data)

    #shorten keys in dict
    data_string = data_string.replace("organicFollowerCount", "organic")
    data_string = data_string.replace("paidFollowerCount", "paid")

    data = json.loads(data_string)
    filtered_data = {'page': page, 'time': time, 'data': data}

    return {data_type: filtered_data}


def page_statistics_filter(data, key, page, time):
    data_type = DATA_TYPES[key]
    data_string = json.dumps(data)

    #shorten keys in dict
    data_string = data_string.replace("pageViews", "v")
    data_string = data_string.replace("PageViews", "")
    data_string = data_string.replace("mobile", "m")
    data_string = data_string.replace("desktop", "d")
    data_string = data_string.replace("Desktop", "D")
    data_string = data_string.replace("Mobile", "M")

    data = json.loads(data_string)
    filtered_data = {'page': page, 'time': time, 'data': data}

    return {data_type: filtered_data}


def share_statistics_filter(data, key, page, time):
    data_type = DATA_TYPES[key]
    filtered_data = {'page': page, 'time': time, 'data': data}

    return {data_type: filtered_data}


