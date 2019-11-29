import base64
import json
import boto3
import os
import timestamp_random as tr
from datetime import datetime as dt


def handler(event, context):
    data_type = event["pathParameters"]["type"]
    data = event["body"]
    timestamp, timestamp_random = IngestUtil.insert_doc(data_type, data=data)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "timestamp": timestamp,
            "id": base64.b64encode(timestamp_random).decode("utf-8")
        })
    }


class IngestUtil:
    __table = None

    @staticmethod
    def get_table():
        if IngestUtil.__table is None:
            client = boto3.resource("dynamodb")
            table_name = os.getenv("DATAPLATTFORM_RAW_TABLENAME")
            table = client.Table(table_name)
            IngestUtil.__table = table
        return IngestUtil.__table

    @staticmethod
    def insert_doc(type, data=None, timestamp=None):
        if data is None:
            return 0, ""
        if timestamp is None:
            timestamp = int(dt.now().timestamp())

        timestamp_random = tr.get_timestamp_random()
        item = {
            "type": type,
            "timestamp_random": timestamp_random,
            "timestamp": timestamp,
            "data": data
        }
        IngestUtil.get_table().put_item(Item=item)

        return timestamp, timestamp_random