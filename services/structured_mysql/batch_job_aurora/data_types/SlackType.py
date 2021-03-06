from data_types.AbstractType import AbstractType
from data_types.slack_util import *


def match_slack_channel(doc):
    """
    :param doc: The slack event dictionary.
    :return: the channel name of an event.
    """
    channel_id = doc["data"]["event"]["channel"]
    return get_slack_channel_name(channel_id)


class SlackType(AbstractType):
    attributes_keep = {
        ("event_type", str): ["data", "event", "type"],
        ("slack_timestamp", int): ["data", "event_time"],
        ("team_id", str): ["data", "team_id"],
        ("channel_name", str, match_slack_channel): []
    }
