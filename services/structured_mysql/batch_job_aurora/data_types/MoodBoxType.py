from data_types.AbstractType import AbstractType


class MoodBoxType(AbstractType):
    attributes_keep = {
    	("time", int): ["data", "time"],
        ("vote", int): ["data", "vote"]
    }
