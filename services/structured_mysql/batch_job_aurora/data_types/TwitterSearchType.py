from data_types.AbstractType import AbstractType

class TwitterSearchType(AbstractType):
    attributes_keep = {
        ("tweet_id", int): ["data", "id"],
        ("created", str): ["data", "created_at"],
        ("text", str): ["data", "text"],
        ("is_retweet", bool): ["data", "is_retweet"],
        ("favourite_count", int): ["data", "favorite_count"],
        ("retweet_count", int): ["data", "retweet_count"],
        ("language", str): ["data", "language"],
        ("hashtags", str): ["data", "hashtags"],
        ("place", str): ["data", "place"],
        ("to_screen_name", str): ["data", "to"]
    }
