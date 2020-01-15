from data_types.AbstractType import AbstractType


class MoodBox(AbstractType):
    attributes_keep = {
    	("time", int): ["data", "time"],
        ("vote", str): ["data", "vote"]
    }
