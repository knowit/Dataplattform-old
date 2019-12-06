from typing import Dict, Union
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


def handler(event, context) -> Dict[str, Union[int, str]]:
    event_code = event['queryStringParameters']['event_code']
    vote_type = event['queryStringParameters']['vote_type']

    event_id = get_event_id_from_event_code(event_code)
    vote_type_valid = is_vote_type_valid(vote_type)

    if event_id and vote_type_valid:
        try:
            increment_vote(event_code, vote_type)
            return {
                'statusCode': 200,
                'body': json.dumps("Event updated successfully")
            }
        except Exception as e:
            print(f"Error: {e}")
            return {
                'statusCode': 500,
                'body': e
            }
    return {
        'statusCode': 500,
        'body': 'Event code or Vote type not valid'
    }


def increment_vote(event_id: str, vote_type: str) -> None:
    sql = f"update EventRatingType set {vote_type}={vote_type}+1 where id='{event_id}'"

    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        connection.commit()
    except pymysql.Error as e:
        print(f"Error: {e}")


def is_vote_type_valid(vote_type: str) -> bool:
    return vote_type in ['positive_count', 'neutral_count', 'negative_count']


def get_event_id_from_event_code(event_code: str) -> Union[str, None]:
    sql = f"SELECT id FROM EventRatingType WHERE active=1 AND event_code='{event_code}'"

    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result['id']
    except Exception as e:
        print(f'Error: {e}')
        return None
