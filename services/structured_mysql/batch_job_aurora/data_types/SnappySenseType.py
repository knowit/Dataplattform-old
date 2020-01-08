from data_types.AbstractType import AbstractType


class SnappySenseType(AbstractType):
	attributes_keep = {
		("location", str): ["data", "location"],
		("co2", int): ["data", "co2"],
		("noise", float): ["data", "noise"],
		("light", int): ["data", "light"],
		("temperature", float): ["data", "temperature"],
		("humidity", float): ["data", "humidity"],
		("movement", bool): ["data", "movement"],
	}
