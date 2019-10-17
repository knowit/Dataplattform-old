import GetOldTweets3 as got
from datetime import datetime
import langid
import urllib.request
import json
from time import strftime


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

TWITTER_SEARCH_LANGUAGE = ["sv", "no"]
TWITTER_SEARCH_TYPE = "TwitterSearchType"

DEFAULT_SINCE_DATE = "2006-01-01"
DEFAULT_LANG = ""
DEFAULT_MAXTWEETS = 5000

langid.set_languages(["no", "nn", "nb", "da", "se", "sv", "en"])

#edit these
ingest_url = ""+TWITTER_SEARCH_TYPE
ingest_api_key = ""


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

def set_criteria(tweetCriteria, lang, maxtweets, from_date, to_date):
    """
    This method sets the criterias for the tweet search.
    If parameters are none, criterias are set to default
    value determined by the script

    :param tweetCriteria: The criteria object
    :param lang: determines the language
    :param maxtweets: determines the max amount of tweets to fetch
    :param from_date: determines start date for search
    :param to_date: determines end date for search
    :return: criteria object
    """
    if lang:
        tweetCriteria.setLang(lang)
    else:
        tweetCriteria.setLang(DEFAULT_LANG)

    if maxtweets:
        tweetCriteria.setMaxTweets(maxtweets)
    else:
        tweetCriteria.setMaxTweets(DEFAULT_MAXTWEETS)

    if from_date:
        tweetCriteria.setSince(from_date)
    else:
        tweetCriteria.setSince(DEFAULT_SINCE_DATE)

    if to_date:
        tweetCriteria.setUntil(to_date)
    else:
        tweetCriteria.setUntil((datetime.now()).strftime("%Y-%m-%d"))

    return tweetCriteria



def setup(query=None, lang=None, maxtweets=None, from_date=None, to_date=None, to_ingest=False):
    """
    This method creates a TweetCriteria object and defines it according to
    the parameters give to the method. Lets the user determine parameters such
    as range of search, searchword and language.

    :param query: what to search for (default=None)
    :param lang: determines language of the tweets to fetch (default=None)
    :param maxtweets: determines the max amount of tweets to fetch (default=None)
    :param from_date: determines start date for search (default=None)
    :param to_date: determines end date for search (default=None)
    :param to_ingest: determines if search results will be posted to ingest (default=False)
    :return: None
    """

    tweetCriteria = got.manager.TweetCriteria()
    tweetCriteria = set_criteria(tweetCriteria, lang, maxtweets, from_date, to_date)

    data_points = search(tweetCriteria, query)
    for data_point in data_points:
        if to_ingest:
            post_to_ingest(data_point)
            print("posting to ingest")

        print(data_point)
    print(len(data_points))

def search(tweetCriteria, query):
    """
    This method searches twitter using GetOldTweets library.
    If no query is given, the method uses the predefined queries from
    TWITTER_SEARCH_ARGS. When query is 'knowit' the method constraints the
    search to tweets in norwegian and swedish only. This is done to mitigate
    the risk of obtaining unrelated tweets

    If a query is give, this method only searches for that keyword

    :param tweetCriteria: the criteria object
    :param query: the query (can be None)
    :return: sorted list (on date) of all tweets found
    """

    data_points = []

    if query:
        tweetCriteria.setQuerySearch(query)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        data_points = filter(tweets, data_points, tweetCriteria.lang)

    else:
        for arg in TWITTER_SEARCH_ARGS:
            tweetCriteria.setQuerySearch(arg)
            if arg == 'knowit':

                for lang in TWITTER_SEARCH_LANGUAGE:
                    tweetCriteria.setLang(lang)
                    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                    data_points = filter(tweets, data_points, tweetCriteria.lang)

                #set language back to all
                tweetCriteria.setLang("")
            else:
                tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                data_points = filter(tweets, data_points, tweetCriteria.lang)

    return sorted(data_points, key=lambda i: i['created_at'])


def filter(tweets, data_points, language):
    """
    This method checks for duplicates and add each tweet in to the list data_points
    It rejects tweets from official knowit accounts and tweets by users having
    knowit in their screen_name

    :param tweets: the tweets to add
    :param data_points: the list where tweets are added
    :param language: language the tweet is written in
    :return: updated list of tweets
    """

    for tweet in tweets:

        # dont fetch tweets from official knowit accounts
        if tweet.username in TWITTER_ACCOUNTS:
            continue

        if "knowit" in tweet.username.lower():
            continue

        tweet_id = tweet.id
        data_point = create_data_point(tweet, language)

        #only add to datapoints if tweet is not there already
        if not any(d['id'] == data_point['id'] for d in data_points):
            data_points.append(data_point)

    return data_points


def create_data_point(item, language):
    """
    This method creates the final record in order to not include all the data available from
    the search. It also identifies retweets and tries to classify the language of the tweet
    in those cases it is not given.

    :param item: the tweet item
    :param language: the language the tweet is written in (can be None)
    :return: data_point (parsed tweet)
    """
    retweet = False
    if item.text.startswith("RT "):
        retweet = True

    if not language:
        language = langid.classify(item.text)[0]

    if language == 'sv':
        language = 'se'

    if language == 'nb' or language == 'nn':
        language = 'no'

    data_point = {
        "id": int(item.id),
        "created_at": item.date.strftime("%Y-%m-%d %H:%M:%S"),
        "text": item.text,
        "is_retweet": retweet,
        "favorite_count": item.favorites,
        "retweet_count": item.retweets,
        "language": language,
        "hashtags": item.hashtags,
        "place": item.geo,
    }
    if item.to:
        if item.to in TWITTER_ACCOUNTS:
            data_point["to"] = item.to

    return data_point


setup(from_date="2019-01-01", to_date="2019-09-27", to_ingest=False)

