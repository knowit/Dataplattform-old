from web_api.api_functions import db_functions
from typing import Dict
import pymysql
import os
import json

connection = pymysql.connect(
    host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
    port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
    user=os.getenv("DATAPLATTFORM_AURORA_USER"),
    password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
    db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


def events_get_handler(event, _) -> Dict[str, int]:
    event_code = event['queryStringParameters']['event_code']
    if event_code:
        result = get_event_from_event_code(event_code)
        return {
            'statusCode': 200,
            'body': result
        }


def get_event_from_event_code(event_code):
    cursor = connection.cursor()

    try:
        cursor.execute(f"SELECT * FROM EventRatingType WHERE active=1 AND event_code='{event_code}'")
    except pymysql.Error as e:
        return {
            'statusCode': 500,
            'body': e
        }

    result = cursor.fetchall()

    return result


def lambda_handler(event, context):
    event_code = event["queryStringParameters"]["name"]
    event_id = is_event_active(event_code)
    if (event_id):
        increment_vote(event_id, "positive_count")
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps("Event updated successfully")
        }
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }


def increment_vote(event_id, vote_type):
    sql = f"update EventRatingType set {vote_type}={vote_type}+1 where id='{event_id}'"

    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"Error: {e}")

    connection.commit()


def is_event_active(event_code):
    sql = f"select id from EventRatingType where active=1 and event_code={event_code}"
    cursor = connection.cursor()
    affected_rows = cursor.execute(sql)
    return cursor.fetchone()['id'] if affected_rows == 1 else False
