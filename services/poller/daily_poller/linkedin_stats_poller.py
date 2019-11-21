import os
import json
import requests_oauthlib
from datetime import datetime
from poller_util import PollerUtil

SCOPE = ['rw_organization_admin',
         'r_organization_social']

LINKEDIN_STATS_TYPE = "LinkedInStatsType"

LINKEDIN_ORGS = {
    "knowit ab": "urn:li:organization:8067",
    "knowit solutions": "urn:li:organization:15179956",
}

LINKEDIN_APIS = {
    "FOLLOWER_STATS_API": "https://api.linkedin.com/v2/organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity=",
    "PAGE_STATS_API": "https://api.linkedin.com/v2/organizationPageStatistics?q=organization&organization=",
    "SHARE_STATS_API": "https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity="
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
            PollerUtil.post_to_ingest_api(data_point, LINKEDIN_STATS_TYPE)

def poll_stats_data(client, organization_id, organization_name):
    data_points = []

    for api in LINKEDIN_APIS.keys():
        query = LINKEDIN_APIS[api]+organization_id
        response = client.get(query)
        data = json.loads(response.content)
        data = filter_stats_data(api, data, organization_name)
        data_points.append(data)

    return data_points


def filter_stats_data(api, data, organization_name):
    data = json.dumps(data)

    if api == "PAGE_STATS_API":

        # shorten allPageViews
        data = data.replace("allPageViews", "all")
        data = data.replace("allDesktopPageViews", "allD")
        data = data.replace("allMobilePageViews", "allM")

        # shorten careersPageViews
        data = data.replace("careersPageViews", "C")
        data = data.replace("desktopCareersPageViews", "dC")
        data = data.replace("mobileCareersPageViews", "mC")

        # shorten jobsPageViews
        data = data.replace("jobsPageViews", "j")
        data = data.replace("desktopJobsPageViews", "dJ")
        data = data.replace("mobileJobsPageViews", "mJ")

        # shorten lifeAtPageViews
        data = data.replace("lifeAtPageViews", "l")
        data = data.replace("desktopLifeAtPageViews", "dL")
        data = data.replace("mobileLifeAtPageViews", 'mL')

        # shorten overviewPageViews
        data = data.replace("overviewPageViews", 'o')
        data = data.replace("desktopOverviewPageViews", "dO")
        data = data.replace("mobileOverviewPageViews", 'mO')

        # shorten insightsPageViews
        data = data.replace("insightsPageViews", "i")
        data = data.replace("desktopInsightsPageViews", "dI")
        data = data.replace("mobileInsightsPageViews", "mI")

        # shorten aboutPageViews
        data = data.replace("aboutPageViews", "a")
        data = data.replace("desktopAboutPageViews", "dA")
        data = data.replace("mobileAboutPageViews", "mA")

        # shorten peoplePageViews
        data = data.replace("peoplePageViews", "pe")
        data = data.replace("desktopPeoplePageViews", "dPe")
        data = data.replace("mobilePeoplePageViews", "mPe")

        # shorten pageStatistics
        data = data.replace("pageStatistics", "pS")

        # shorten pageViews
        data = data.replace("pageViews", "pV")

    elif api == "FOLLOWER_STATS_API":

        # change followerCounts to fC
        data = data.replace("followerCounts", "fC")
        # change organicFollowerCount to ofC
        data = data.replace("organicFollowerCount", "ofC")
        # change paidFollowerCount to pfC
        data = data.replace("paidFollowerCount", "pfC")

    data = json.loads(data)

    # remove paging (pop)
    data.pop('paging')

    retrieved = datetime.now().timestamp()

    # add metadata
    filtered_data = {'retrieved': retrieved, 'name': organization_name, 'source': api, 'data': data}
    return filtered_data


