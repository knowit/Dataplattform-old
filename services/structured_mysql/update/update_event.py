import pymysql
import time
import os
import json

TYPE = "EventRatingType"

def handler(event, context):

    data_type = event["pathParameters"]["type"]

    if data_type != TYPE:
        return {
            'statusCode': 400,
            'body': 'unexpected type'
        }

    timestamp_now = str(int(time.time()))

    data = json.loads(event["body"])
    response = update_event(data, timestamp_now)

    if response > 0:
        return {
            'statusCode': 200,
            'body': 'update successful'
        }
    else:
        return {
            'statusCode': 500,
            'body': 'update unsuccessful'
        }


def update_event(data, timestamp_now):

    connection = connect_to_aurora()
    button_id = data["event_button_id"]

    record = get_record(connection, button_id, timestamp_now)

    if record:
        if record["positive_count"]:
            updated_pos_count = record["positive_count"] + data["positive_count"]
        else:
            updated_pos_count = data["positive_count"]

        if record["neutral_count"]:
            updated_neu_count = record["neutral_count"] + data["neutral_count"]
        else:
            updated_neu_count = data["neutral_count"]

        if record["negative_count"]:
            updated_neg_count = record["negative_count"] + data["negative_count"]
        else:
            updated_neg_count = data["negative_count"]

        response = update_record(connection, record["id"], updated_pos_count, updated_neu_count, updated_neg_count)
        connection.close()
        return response

    connection.close()
    return -1

def get_record(connection, button_id, timestamp_now):
    cur = connection.cursor()
    sql_query = "SELECT * FROM Dataplattform.EventRatingType2 WHERE event_button_id = "+str(button_id)+\
                " AND (timestamp_from + 60 * 15 < "+timestamp_now+" AND timestamp_to + 60 * 15 > "+\
                timestamp_now+");"

    try:
        response = cur.execute(sql_query)
    except pymysql.err.Error:
        cur.close()
        return None

    if response == 0:
        cur.close()
        return None

    record = cur.fetchall()[0]
    cur.close()
    return record

def update_record(connection, record_id, updated_pos_count, updated_neu_count, updated_neg_count):
    cur = connection.cursor()
    sql_query = "UPDATE Dataplattform.EventRatingType2 SET positive_count = "+str(updated_pos_count)+\
                ", neutral_count = "+str(updated_neu_count)+", negative_count = "+str(updated_neg_count)+\
                " WHERE id = \""+record_id+"\";"

    try:
        response = cur.execute(sql_query)
    except pymysql.err.Error:
        cur.close()
        return -1

    connection.commit()
    cur.close()
    return response


def connect_to_aurora():
    return pymysql.connect(
        host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

