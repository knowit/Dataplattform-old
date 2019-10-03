from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from poller_util import PollerUtil
import os


TWITTER_SEARCH_TYPE = "TwitterSearchType"
TWITTER_SEARCH_LANGUAGE = ["se", "no"]
TWITTER_SEARCH_ARGS = ['knowit', '"knowit objectnet"', '"knowit amende"',
                       '"knowit solutions"', 'knowit norge', '"knowit stavanger"',
                       '"knowit experience"', 'knowit bergen', 'knowit oslo',
                       '"knowit insight"', 'knowit norway', 'knowit sweden',
                       'knowit finland']


TWITTER_ACCOUNTS = [
    "knowitnorge",
    "knowitab",
    "KnowitSuomi"
]


def authenticate():

    auth = OAuthHandler(os.getenv("DATAPLATTFORM_TWITTER_CONSUMER_KEY"), os.getenv("DATAPLATTFORM_TWITTER_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("DATAPLATTFORM_TWITTER_ACCESS_TOKEN"), os.getenv("DATAPLATTFORM_TWITTER_ACCESS_SECRET"))
    return API(auth)

def poll():
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
    #search for knowit-related tweets related
    data_points = []

    for arg in TWITTER_SEARCH_ARGS:
        #need to restrict 'knowit' search to avoid gibberish
        if arg == 'knowit':
            search = Cursor(api.search, q=arg, lang=("no" or "se"), since_id=last_inserted_id, tweet_mode='extended').items()
            data_points = extract_search_data(search, data_points)
        else:
            search = Cursor(api.search, q=arg, since_id=last_inserted_id, tweet_mode='extended').items()
            data_points = extract_search_data(search, data_points)

    return sorted(data_points, key=lambda i: i['id'])

def extract_search_data(search, datapoints):
    for item in search:

        #dont fetch tweets from official knowit accounts
        if item.user.screen_name in TWITTER_ACCOUNTS:
            continue

        if 'knowit' in item.user.screen_name.lower():
            continue

        tweet_id = item.id
        data_point = create_data_point(item)

        #only add to datapoints if tweet is not there already
        if not any(d['id'] == tweet_id for d in datapoints):
            datapoints.append(data_point)

    return datapoints


def create_data_point(item):
    #check for old school retweeting method
    if item.retweeted == False and item.full_text.startswith("RT @"):
        item.retweeted = True

    hashtags = ""
    if item.entities['hashtags']:
        for hashtag in item.entities['hashtags']:
            hashtags += hashtag['text'] + ", "
        hashtags = hashtags[:-2]

    if item.place:
        item.place = item.place.full_name

    return {
        "id": item.id,
        "created_at": str(item.created_at),
        "text": item.full_text,
        "retweeted": item.retweeted,
        "retweet_count": item.retweet_count,
        "favorite_count": item.favorite_count,
        "language": item.lang,
        "hashtags": hashtags,
        "place": item.place,
    }

