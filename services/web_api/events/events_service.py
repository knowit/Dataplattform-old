import pymysql
import json
import time
from typing import Dict, Union
from api_functions.db_functions import get_db_connection


def get_events(event):
    query_params = event['queryStringParameters']

    creator = query_params['creator'] if query_params['creator'] else None
    future = query_params['time_from'] if query_params['time_from'] else None
    previous = query_params['time_to'] if query_params['time_to'] else None
    active = query_params['active'] if query_params['active'] else None

    if creator:
        return get_events_for_creator(creator)
    if future:
        return get_future_events(future)
    if previous:
        return get_previous_events(previous)
    if active:
        return get_active_events()

    return get_all_events()


def get_events_for_creator(creator):
    sql = f"SELECT * FROM EventRatingType WHERE creator='{creator}'"
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"Error: {e}")
    return cursor.fetchall()


def get_future_events(days):
    connection = get_db_connection()
    cursor = connection.cursor()

    time_now = int(time.time())
    days_int = int(days)

    sql = (f"SELECT * FROM EventRatingType "
           f"WHERE timestamp_to > unix_timestamp() "
           f"AND timestamp_to < unix_timestamp() + 60*60*24*{days_int} ")
    try:
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"Error: {e}")
    return cursor.fetchall()


def get_previous_events(days):
    connection = get_db_connection()
    cursor = connection.cursor()

    time_now = int(time.time())
    days_int = int(days)

    sql = (f"SELECT * FROM EventRatingType "
           f"WHERE timestamp_from < unix_timestamp() "
           f"AND timestamp_from > unix_timestamp() - 60*60*24*{days_int} ")
    try:
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"Error: {e}")
    return cursor.fetchall()


def get_active_events():
    return None


def get_all_events():
    return None


def patch_event(event):
    event_code = event['queryStringParameters']['event_code']
    vote_type = event['queryStringParameters']['vote_type']

    event_id = get_event_id_from_event_code(event_code)
    vote_type_valid = is_vote_type_valid(vote_type)

    if event_id and vote_type_valid:
        try:
            increment_vote(event_id, vote_type)
            return {
                'statusCode': 204,
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
    connection = get_db_connection()
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
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result['id']
    except Exception as e:
        print(f'Error: {e}')
        return None
