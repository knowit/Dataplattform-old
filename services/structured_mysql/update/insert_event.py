import os
import pymysql


def handler(event, context):

    connection = pymysql.connect(
        host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    ids = insert_events(connection, event['data'], get_saved_events(connection))

    for id in ids:
        sql = 'DELETE FROM EventRatingType2 WHERE id = "' + id['id'] + '";'
        cur = connection.cursor()
        try:
            cur.execute(sql)
        except pymysql.err.IntegrityError:
            print("Failed")

    connection.commit()
    connection.close()

    return {
        'statusCode': 200,
        'body': ''
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
                        "FROM EventRatingType2 " \
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


def insert_events(db_connection, calendar, ids):

    for event in calendar:

        for rating_box in calendar[event]['event_button_name']:
            box_id = get_box_id(rating_box, db_connection)
            if len(box_id) == 0:
                break

            for id in ids:
                if id['event_id'] == event and box_id[0]["event_button_id"] == id['event_button_id']:
                    ids.remove(id)

            if box_id[0]["event_button_name"] == rating_box:
                parameters = "id, event_id"
                values = '"' + event + str(box_id[0]["event_button_id"]) + '", "' + event + '"'
                for parameter in calendar[event]:
                    parameters += ", " + parameter
                    if parameter == "event_button_name":
                        values += ", \"" + rating_box + "\""
                    else:
                        if type(calendar[event][parameter]) is str:
                            values += ', "' + str(calendar[event][parameter]) + '"'
                        else:
                            values += ", " + str(calendar[event][parameter])
                sql = "INSERT IGNORE INTO EventRatingType2 (" \
                      + parameters \
                      + ", " + "event_button_id" + ") VALUES (" \
                      + values + ", " \
                      + str(box_id[0]["event_button_id"]) \
                      + ");"
                cursor = db_connection.cursor()
                try:
                    cursor.execute(sql)
                except pymysql.err.IntegrityError:
                    print("duplicate")
                    break
    return ids
