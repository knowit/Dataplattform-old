from tweepy import OAuthHandler
from tweepy import API
import json
import urllib.request

TWITTER_ACCOUNT_TYPE = "TwitterAccountType"

TWITTER_ACCOUNTS = {
    "knowitnorge": "TwitterAccountKnowitnorgeType",
    "knowitab": "TwitterAccountKnowitabType",
    "knowitx": "TwitterAccountKnowitxType"
}

#edit these
twitter_consumer_key = ""
twitter_consumer_secret = ""
twitter_access_token = ""
twitter_access_secret = ""

ingest_url = ""+TWITTER_ACCOUNT_TYPE
ingest_api_key = ""

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

def setup(min_id=None, max_id=None, to_ingest=False):
    api = authenticate()

    for account in TWITTER_ACCOUNTS:
        data_points = get_account_data(api, account, min_id, max_id)
        for data_point in data_points:
            if to_ingest:
                print("posting to ingest")
                post_to_ingest(data_point)

            print(data_point)

        exit(0)


def get_account_data(api, account, min_id, max_id):
    """
    This method searches the timeline of the given account using the user_timeline API from twitter
    to see if new tweets are available. It uses last_inserted_id to constrain the search and searches
    for tweets up to seven days back

    :param api: the api object
    :param account: the account to get data from
    :param min_id: dont fetch tweets older than this id
    :param max_id: dont fetch tweets newer than this id
    :return: data_points: the tweets found
    """

    data_points = []
    page_num = 1

    timeline = api.user_timeline(screen_name=account, page=page_num, min_id=min_id, max_id=max_id, tweet_mode='extended')
    while timeline:
        for item in timeline:
            data_point = create_data_point(item)
            data_points.append(data_point)

        page_num += 1
        timeline = api.user_timeline(screen_name=account, page=page_num, min_id=min_id, max_id=max_id, tweet_mode='extended')

    return sorted(data_points, key=lambda i: i['created_at'])


def create_data_point(item):
    """
    This method creates the final record in order to not include all the data available from
    the search. It also identifies retweets and parse hashtags and mentions as a string

    :param item: the tweet item
    :return: the parsed tweet
    """
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


setup(max_id=1177485166110883840, to_ingest=False)
