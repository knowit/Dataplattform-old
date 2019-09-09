import decimal
import json
import urllib.request
import urllib.parse
import os
import pymysql
from datetime import datetime as dt

sql_queries = {
    'MyTestType': 'SELECT * FROM MyTestType',
    'Testing':'SELECT COUNT(*) FROM MyTestType',
    'Testing2':'SELECT COUNT(*) FROM MyTestType WHERE testBool=true',
    'SlackEmojiType': 'SELECT * FROM SlackEmojiType'
}


def handler(event, context):
    data_type = event["pathParameters"]["data_type"]
    connection = pymysql.connect(
        host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    if data_type not in sql_queries:
        return{
            'statusCode': 404,
            'body': 'Data_type not found'
        }
    sql_query = sql_queries[data_type]

    success, data = pull_data(connection, sql_query)

    if not success:
        return{
            'statusCode': 404,
            'body': 'No table found.'
        }

    return{
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data, default=decimal_default)
    }


def pull_data(sql_connection, sql_query):
    cur = sql_connection.cursor()

    success = True
    data = ""
    try:
        cur.execute(sql_query)
        data = cur.fetchall()
    except pymysql.err.ProgrammingError:
        success = False
        print("No table found")
    finally:
        sql_connection.close()

    return success, data


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
