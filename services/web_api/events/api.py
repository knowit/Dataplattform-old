from web_api.api_functions import db_functions
from typing import Dict
import pymysql

db_connection = db_functions.get_db_connection()


def get_event_code(event, _) -> Dict[str, int]:
    event_code_id = event.pathParameters.id
    cursor = db_connection.cursor()

    try:
        cursor.execute(f"SELECT * FROM EventRatingType WHERE event_code='{event_code_id}'")
    except pymysql.Error as e:
        return {
            'statusCode': 500,
            'body': e
        }

    result = cursor.fetchall()

    return {
        'statusCode': 200,
        'body': result
    }
