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
    auth = OAuthHandler(os.getenv("DATAPLATTFORM_TWITTER_CONSUMER_KEY"), os.getenv("DATAPLATTFORM_TWITTER_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("DATAPLATTFORM_TWITTER_ACCESS_TOKEN"), os.getenv("DATAPLATTFORM_TWITTER_ACCESS_SECRET"))
    return API(auth)


def poll():
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

        data_points = []
        page_num = 1

        timeline = api.user_timeline(screen_name=account, since_id=last_inserted_id, page=page_num, tweet_mode='extended')
        while timeline:
            for item in timeline:
                if item.created_at.date() < week_ago:
                    return sorted(data_points, key=lambda i: i['id'])

                data_point = create_data_point(item)
                data_points.append(data_point)

            page_num += 1
            timeline = api.user_timeline(screen_name=account, since_id=last_inserted_id, page=page_num, tweet_mode='extended')

        return sorted(data_points, key=lambda i: i['id'])


def create_data_point(item):
    # check for old school retweeting method
    if item.retweeted == False and item.full_text.startswith("RT @"):
        item.retweeted = True

    # hashtags as string
    hashtags = ""
    if item.entities['hashtags']:
        for hashtag in item.entities['hashtags']:
            hashtags += hashtag['text']+", "
        hashtags = hashtags[:-2]

    # mentions as string
    mentions = ""
    if item.entities['user_mentions']:
        for mention in item.entities['user_mentions']:
            mentions += mention['screen_name']+", "
        mentions = mentions[:-2]

    return {
        "id": item.id,
        "created_at": str(item.created_at),
        "user_screen_name": item.user.screen_name,
        "text": item.full_text,
        "retweeted": item.retweeted,
        "retweet_count": item.retweet_count,
        "favorite_count": item.favorite_count,
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



