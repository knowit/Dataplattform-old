import json
import os
import urllib.parse
import urllib.request

# This dictionary will be used for caching information about a specific channel id and therefore
# saving a lot of time using the slack API.
slack_channel_id_to_channel_info = {}


def fetch_from_api(base_url, params):
    """
    A helping method for fetching from API.
    :param base_url: The base API url.
    :param params: All the params keys and values needed excluding token.
    :return: the response fetched.
    """
    token = os.getenv("DATAPLATTFORM_OAUTH_SLACK_TOKEN")
    params["token"] = token

    query = urllib.parse.urlencode(params)
    url = base_url + "?" + query
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode())


def fetch_slack_channel_info(channel_id):
    """
    This method fetches the channel_info using slack's API and saves it in the dict
    `slack_channel_id_to_channel_info`.
    :param channel_id: Which channel should be fetched.
    :return:
    """
    params = {"channel": channel_id}
    base_url = "https://slack.com/api/channels.info"
    channel = fetch_from_api(base_url, params)
    slack_channel_id_to_channel_info[channel_id] = channel


def get_slack_channel_name(channel_id):
    if channel_id not in slack_channel_id_to_channel_info:
        fetch_slack_channel_info(channel_id)
    channel = slack_channel_id_to_channel_info[channel_id]
    if not channel["ok"]:
        return None
    return channel["channel"]["name"]
