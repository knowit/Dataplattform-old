from tweepy import OAuthHandler
from tweepy import API
import json
import urllib.request

TWITTER_ACCOUNT_TYPE = "TwitterAccountType"

TWITTER_ACCOUNTS = {
    #"knowitnorge": "TwitterAccountKnowitnorgeType",
    #"knowitab": "TwitterAccountKnowitabType",
    "knowitx": "TwitterAccountKnowitxType"
}

#edit these
twitter_consumer_key = "cdfOmsHN8u8QoJIhQjnKARy4p"
twitter_consumer_secret = "Q7yDKpAB9Qa2259XLZTXYswMN7ApVJHwgA8vLgMWnzAZK2Vw0Z"
twitter_access_token = "1167428599458271232-DLmCV6eBSS0gFNfEglpM1CYfgsKL9V"
twitter_access_secret = "XuKn2UFsqkDX0tnRo6YwEMy2N27alwTd5McM5iH5yn7vN"

ingest_url = "https://2q8h3bkh73.execute-api.eu-central-1.amazonaws.com/prod/dataplattform_ingest/"+TWITTER_ACCOUNT_TYPE
ingest_api_key = "GK4obGHhUf9hWfXyGPds99BKQet3lWej2nqnz9Ux"

def authenticate():
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_secret)
    return API(auth)

def post_to_ingest(data):
    """
    Posts data to ingest defined by ingest_url
    :param data: the data point to be posted
    :return: repsone code from ingest
    """
    data = json.dumps(data).encode()
    try:
        request = urllib.request.Request(ingest_url, data=data, headers={"x-api-key": ingest_api_key})
        response = urllib.request.urlopen(request)
        return response.getcode()
    except urllib.request.HTTPError:
        return 500

def setup(from_date=None, to_date=None, to_ingest=False):
    api = authenticate()

    for account in TWITTER_ACCOUNTS:
        data_points = get_account_data(api, account)
        for data_point in data_points:
            if to_ingest:
                print("posting to ingest")

            print(data_point)

        exit(0)


def get_account_data(api, account):

        data_points = []
        page_num = 1
        timeline = api.user_timeline(screen_name=account, page=page_num, tweet_mode='extended')
        while timeline:
            for item in timeline:
                data_point = create_data_point(item)
                data_points.append(data_point)

            page_num += 1
            timeline = api.user_timeline(screen_name=account, page=page_num, tweet_mode='extended')

        return sorted(data_points, key=lambda i: i['created_at'])


def create_data_point(item):
    # check for old school retweeting method
    retweet = False
    if item.full_text.startswith("RT @"):
        retweet = True

    # hashtags as string
    hashtags = ""
    if item.entities['hashtags']:
        for hashtag in item.entities['hashtags']:
            hashtags += hashtag['text']+" "
        hashtags = hashtags[:-1]

    # mentions as string
    mentions = ""
    if item.entities['user_mentions']:
        for mention in item.entities['user_mentions']:
            mentions += mention['screen_name']+" "
        mentions = mentions[:-1]

    return {
        "id": item.id,
        "created_at": str(item.created_at),
        "user_screen_name": item.user.screen_name,
        "text": item.full_text,
        "is_retweet": retweet,
        "favorite_count": item.favorite_count,
        "retweet_count": item.retweet_count,
        "language": item.lang,
        "hashtags": hashtags,
        "mentions": mentions,
        "user_name": item.user.name,
        "user_statuses_count": item.user.statuses_count,
        "user_followers_count": item.user.followers_count,
        "user_favourites_count": item.user.favourites_count,
        "user_friends_count": item.user.friends_count,
        "user_listed_count": item.user.listed_count
    }


setup(to_ingest=True)