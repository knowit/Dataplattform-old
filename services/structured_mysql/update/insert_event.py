import os
import pymysql
import json


def handler(event, context):
    print("//////////////////////////////////////RUNNING///////////////////////////////")
    connection = pymysql.connect(
        host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    saved_events = get_saved_events(connection)
    data = {}
    for records in event['Records']:
        data.update(json.loads(records['Sns']['Message'])['data'])
    ids = saved_events
    if len(data) > 0:
        ids = insert_events(connection, data, saved_events)
    for id in ids:
        sql = 'DELETE FROM EventRatingType WHERE id = "' + id['id'] + '";'
        cur = connection.cursor()
        try:
            cur.execute(sql)
        except pymysql.err.IntegrityError:
            print("Failed")
    connection.commit()
    connection.close()

    return {
        'statusCode': 200,
        'body': 'Done'
        }


def get_box_id(box_name, db_connection):
    cursor = db_connection.cursor()
    sql = 'SELECT * FROM EventBoxes WHERE event_button_name = "' + box_name + '";'
    try:
        cursor.execute(sql)
    except pymysql.err.IntegrityError:
        return
    return cursor.fetchall()


def get_saved_events(db_connection):
    getSavedEventsSql = "SELECT id, event_id, event_button_id " \
                        "FROM EventRatingType " \
                        "WHERE ( timestamp_from < unix_timestamp() + 60*60*24 " \
                        "OR timestamp_to < unix_timestamp() + 60*60*24) " \
                        "AND (timestamp_from > unix_timestamp() " \
                        "OR timestamp_to > unix_timestamp());"
    cur = db_connection.cursor()
    ids = {}
    try:
        cur.execute(getSavedEventsSql)
        ids = cur.fetchall()
    except pymysql.err.IntegrityError:
        print("Failed")
    return ids


def insert_events(db_connection, events, ids):
    for event in events:
        for entry in range(len(events[event]['event_button_name'])+1):
            parameters = "id, event_id"
            values = ""
            box_id = []
            if entry < len(events[event]['event_button_name']):
                box_id = get_box_id(events[event]['event_button_name'][entry], db_connection)
            for id in ids:
                if id['event_id'] == event:
                    if entry >= len(events[event]['event_button_name']):
                        ids.remove(id)
                    else:
                        if len(box_id) == 0:
                            break
                        if box_id[0]['event_button_id'] == id['event_button_id']:
                            ids.remove(id)

            if entry >= len(events[event]['event_button_name']):
                values += '"' + event + '", "' + event + '"'
            else:
                values = '"' + event + json.dumps(box_id[0]["event_button_id"]) + '", "' + event + '"'

            for parameter in events[event]:
                if entry < len(events[event]['event_button_name']) or parameter != "event_button_name":
                    parameters += ", " + parameter
                if parameter == "event_button_name":
                    if entry < len(events[event]['event_button_name']):
                        values += ", \"" + events[event]['event_button_name'][entry] + "\""
                else:
                    values += ", " + json.dumps(events[event][parameter], ensure_ascii=False)

            sql = "INSERT IGNORE INTO EventRatingType (" + parameters
            if entry < len(events[event]['event_button_name']):
                sql += ", event_button_id"
            sql += ") VALUES (" \
                + values
            if entry < len(events[event]['event_button_name']):
                sql += ", " + str(box_id[0]["event_button_id"])
            sql += ");"
            cursor = db_connection.cursor()
            print("///////////////////////////////////SQL/////////////////////////////")
            print(sql)
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                print("duplicate")
    return ids
