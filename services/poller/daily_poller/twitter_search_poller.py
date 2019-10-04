from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from poller_util import PollerUtil
import os


TWITTER_SEARCH_TYPE = "TwitterSearchType"
TWITTER_SEARCH_LANGUAGE = ["se", "no"]
TWITTER_SEARCH_ARGS = ['knowit', '"knowit objectnet"', '"knowit amende"',
                       '"knowit solutions"', '"knowit experience"', '"knowit insight"',
                       'knowitab', 'knowitnorge', 'knowit norge', '"knowit stavanger"',
                       'knowit bergen', 'knowit oslo', 'knowit sverige', 'knowit norway',
                       'knowit sweden', 'knowit finland', 'knowitx']


TWITTER_ACCOUNTS = [
    "knowitnorge",
    "knowitab",
    "KnowitSuomi",
    "knowitx"
]


def authenticate():
    """
    This method authenticates against twitter API
    :return: api object
    """

    auth = OAuthHandler(os.getenv("DATAPLATTFORM_TWITTER_CONSUMER_KEY"), os.getenv("DATAPLATTFORM_TWITTER_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("DATAPLATTFORM_TWITTER_ACCESS_TOKEN"), os.getenv("DATAPLATTFORM_TWITTER_ACCESS_SECRET"))
    return API(auth)

def poll():
    """
    This method calls the poll_search_data method and is returned new tweets.
    If new tweets are found, these get put in to dynamoDB and last_inserted_id is updated
    :return: True
    """
    api = authenticate()

    last_inserted_doc = PollerUtil.fetch_last_inserted_doc(TWITTER_SEARCH_TYPE)
    last_inserted_id = 1
    if last_inserted_doc:
        last_inserted_id = int(last_inserted_doc)

    data_points = poll_search_data(api, last_inserted_id)

    for data_point in data_points:
        result = PollerUtil.post_to_ingest_api(data_point, TWITTER_SEARCH_TYPE)
        if result is not None:
            last_inserted_id = data_point['id']

    PollerUtil.upload_last_inserted_doc(last_inserted_id, TWITTER_SEARCH_TYPE)


    return True

def poll_search_data(api, last_inserted_id):
    """
    This method searches twitter using the twitter search API.
    It uses the queries predefined in TWITTER_SEARCH ARGS.
    When query is 'knowit' the method constraints the search to tweets in norwegian and swedish only.
    This is done to mitigate the risk of obtaining unrelated tweets.
    The search is also constrained by last_inserted_id

    The twitter search API does not support searches for older than 7 days back

    :param api: api object
    :param last_inserted_id:
    :return: data_points: tweets found
    """
    data_points = []

    for arg in TWITTER_SEARCH_ARGS:
        #need to restrict 'knowit' search to avoid gibberish
        if arg == 'knowit':
            search = Cursor(api.search, q=arg, lang=("no" or "se"), since_id=last_inserted_id, tweet_mode='extended').items()
            data_points = filter_search_data(search, data_points)
        else:
            search = Cursor(api.search, q=arg, since_id=last_inserted_id, tweet_mode='extended').items()
            data_points = filter_search_data(search, data_points)

    return sorted(data_points, key=lambda i: i['created_at'])


def filter_search_data(search, data_points):
    """
    This method filters tweet found for the different query searches.
    It checks for duplicates in data_points and rejects tweets
    done by official knowit accoints defined in TWITTER_ACCOUNTS
    and tweets done by user with knowit in their screen name

    :param search: the search result
    :param data_points: list of tweets found so far
    :return: data_point: updated with new tweets
    """
    for item in search:

        #dont fetch tweets from official knowit accounts
        if item.user.screen_name in TWITTER_ACCOUNTS:
            continue

        if 'knowit' in item.user.screen_name.lower():
            continue

        tweet_id = item.id
        data_point = create_data_point(item)

        #only add to datapoints if tweet is not there already
        if not any(d['id'] == tweet_id for d in data_points):
            data_points.append(data_point)

    return data_points


def create_data_point(item):
    """
    This method creates the final record in order to not include all the data available from
    the search. It also identifies retweets and parse hashtags as a string

    :param item: the tweet item
    :return: the parsed tweet
    """
    retweet = False
    if item.full_text.startswith("RT @"):
        retweet = True

    hashtags = ""
    if item.entities['hashtags']:
        for hashtag in item.entities['hashtags']:
            hashtags += hashtag['text'] + " "
        hashtags = hashtags[:-1]

    if item.place:
        item.place = item.place.full_name

    data_point = {
        "id": item.id,
        "created_at": str(item.created_at),
        "text": item.full_text,
        "is_retweet": retweet,
        "favorite_count": item.favorite_count,
        "retweet_count": item.retweet_count,
        "language": item.lang,
        "hashtags": hashtags,
        "place": item.place,
    }
    if item.in_reply_to_screen_name:
        if item.in_reply_to_screen_name in TWITTER_ACCOUNTS:
            data_point["to"] = item.in_reply_to_screen_name

    return data_point
