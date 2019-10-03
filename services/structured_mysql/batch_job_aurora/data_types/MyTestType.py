from data_types.AbstractType import AbstractType


''' 
This file is used for testing different attribute types in ingest

Example data:
{
    "data":{
            "testString":"StringHere",
            "testInt":237,
            "testBool":true
            }
}
'''


class MyTestType(AbstractType):
    attributes_keep = {
        ("testString", str): ["data", "testString"],
        ("testInt", int): ["data", "testInt"],
        ("testBool", bool): ["data", "testBool"]
    }