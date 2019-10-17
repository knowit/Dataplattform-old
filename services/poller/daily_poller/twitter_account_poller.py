from tweepy import OAuthHandler
from tweepy import API
from datetime import datetime
from datetime import timedelta
from poller_util import PollerUtil
import os

TWITTER_ACCOUNT_TYPE = "TwitterAccountType"


TWITTER_ACCOUNTS = {
    "knowitnorge": "TwitterAccountKnowitnorgeType",
    "knowitab": "TwitterAccountKnowitabType",
    "knowitx": "TwitterAccountKnowitxType"
}


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
    This method calls the poll_account_data with the defined accounts in TWITTER_ACCOUNTS
    and is returned new tweets. If new tweets are found, these get put in to dynamoDB
    and last_inserted_id is updated
    :return: True
    """
    api = authenticate()

    week_ago = (datetime.now() - timedelta(days=7)).date()


    for account in TWITTER_ACCOUNTS:

        last_inserted_doc = PollerUtil.fetch_last_inserted_doc(TWITTER_ACCOUNTS[account])
        last_inserted_id = 1
        if last_inserted_doc:
            last_inserted_id = int(last_inserted_doc)

        data_points = poll_account_data(api, account, last_inserted_id, week_ago)

        for data_point in data_points:
            result = PollerUtil.post_to_ingest_api(data_point, TWITTER_ACCOUNT_TYPE)
            if result is not None:
                last_inserted_id = data_point['id']

        PollerUtil.upload_last_inserted_doc(last_inserted_id, TWITTER_ACCOUNTS[account])

    return True


def poll_account_data(api, account, last_inserted_id, week_ago):
        """
        This method searches the timeline of the given account using the user_timeline API from twitter
        to see if new tweets are available. It uses last_inserted_id to constrain the search and searches
        for tweets up to seven days back

        :param api: the api object
        :param account: the account to get data from
        :param last_inserted_id: id of the latest tweet inserted by this poller
        :param week_ago: the date at one week ago
        :return: data_points: the tweets found
        """
        data_points = []
        page_num = 1

        timeline = api.user_timeline(screen_name=account, since_id=last_inserted_id, page=page_num, tweet_mode='extended')
        while timeline:
            for item in timeline:
                if item.created_at.date() < week_ago:
                    return sorted(data_points, key=lambda i: i['created_at'])

                data_point = create_data_point(item)
                data_points.append(data_point)

            page_num += 1
            timeline = api.user_timeline(screen_name=account, since_id=last_inserted_id, page=page_num, tweet_mode='extended')

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



