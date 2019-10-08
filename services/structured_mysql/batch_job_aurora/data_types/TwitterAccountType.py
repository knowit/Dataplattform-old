from data_types.AbstractType import AbstractType

class TwitterAccountType(AbstractType):
    attributes_keep = {
        ("tweet_id", int): ["data", "id"],
        ("created", str): ["data", "created_at"],
        ("user_screen_name", str): ["data", "user_screen_name"],
        ("text", str): ["data", "text"],
        ("is_retweet", bool): ["data", "is_retweet"],
        ("favourite_count", int): ["data", "favorite_count"],
        ("retweet_count", int): ["data", "retweet_count"],
        ("language", str): ["data", "language"],
        ("hashtags", str): ["data", "hashtags"],
        ("mentions", str): ["data", "mentions"],
        ("user_name", str): ["data", "user_name"],
        ("user_statuses_count", int): ["data", "user_statuses_count"],
        ("user_followers_count", int): ["data", "user_followers_count"],
        ("user_favourites_count", int): ["data", "user_favourites_count"],
        ("user_friends_count", int): ["data", "user_friends_count"],
        ("user_listed_count", int): ["data", "user_listed_count"]
    }
