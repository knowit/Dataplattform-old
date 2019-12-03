import os
import pymysql
import json
from random import randint
from insert_event_util import EventSQLs


def handler(event, context):
    db_connection = _get_db_connection()

    google_events = _get_google_events(event)
    db_events = _get_events_from_db_which_are_active_the_next_24_hours(db_connection)

    queries = EventSQLs(db_connection, db_events)

    # Construct DELETE queries for deleted google events from db
    google_event_ids = list(google_events.keys())
    for db_event in db_events:
        if db_event['event_id'] not in google_event_ids:
            queries.append_delete_queries_from_event(db_event)

    # Construct INSERT and UPDATE queries for added or updated google events in db
    db_event_ids = list([db_event['event_id'] for db_event in db_events])
    for (google_event_id, google_event) in google_events.items():
        google_event['event_id'] = str(google_event_id)

        # get event_code from db_events or generate a new event_code
        if google_event_id in db_event_ids:
            db_event_code = [e['event_code'] for e in db_events if e['event_id'] == google_event_id].pop(0)
            google_event['event_code'] = db_event_code
        else:
            google_event['event_code'] = queries.generate_event_code()

        queries.append_insert_or_update_queries_from_event(google_event)

    # Execute sql queries so that db is in sync with google calendar
    queries.execute_sql_queries()
    db_connection.commit()
    db_connection.close()

    return {
        'statusCode': 200,
        'body': 'Done'
    }


def _get_db_connection() -> pymysql.Connection:
    return pymysql.connect(
        host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


def _get_google_events(event):
    google_events = {}
    for records in event['Records']:
        google_event = json.loads(records['Sns']['Message'])['data']
        google_events.update(google_event)

    return google_events


def _get_events_from_db_which_are_active_the_next_24_hours(db_connection):
    getSavedEventsSql = "SELECT id, event_id, event_button_id, event_code " \
                        "FROM EventRatingType " \
                        "WHERE ( timestamp_from < unix_timestamp() + 60*60*24 " \
                        "OR timestamp_to < unix_timestamp() + 60*60*24) " \
                        "AND (timestamp_from > unix_timestamp() " \
                        "OR timestamp_to > unix_timestamp());"
    cursor = db_connection.cursor()
    db_events = {}
    try:
        cursor.execute(getSavedEventsSql)
        db_events = cursor.fetchall()
    except pymysql.err.Error as e:
        print(f"Failed to get saved events: {e}")
    print("IDS")
    print(db_events)
    return db_events


if __name__ == '__main__':
    event = {
        "Records": [{
            "Sns": {
                "Message": json.dumps({
                    "data": {
                        "3mbuq0b4pciqef8qghu4ouc715": {
                            "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                            "timestamp_from": 1575381600, "timestamp_to": 1575396000,
                            "event_summary": "Rust kodekveld", "event_button_name": [],
                            "creator": "thomas.tokje@knowit.no"},
                        "5sp3pome607cff0pktahpve6pc": {
                            "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                            "timestamp_from": 1575387900, "timestamp_to": 1575391500,
                            "event_summary": "Speech training with Oslo Speaking Club",
                            "event_button_name": [], "creator": "alina.kay@knowit.no"},
                        "755fd38mdr0egjo8i5i6h2lt0l": {
                            "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                            "timestamp_from": 1575554400, "timestamp_to": 1575561600,
                            "event_summary": "3D-printerkveld", "event_button_name": [],
                            "creator": "ab@knowit.no"},
                        "6bu90333au1rks6sv6370t9qk6": {
                            "calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                            "timestamp_from": 1576076400, "timestamp_to": 1576083600,
                            "event_summary": "Knowit Objectnet Mangekamp: Bowling", "event_button_name": [],
                            "creator": "aulon.mujaj@knowit.no"},
                        "06vllccjqsurk9t7jr695fdnai": {
                            "calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                            "timestamp_from": 1576191600, "timestamp_to": 1576278000,
                            "event_summary": "Julebord", "event_button_name": ['alfa'],
                            "creator": "marius.backer@knowit.no"}
                    }
                })
            }
        }
        ]
    }
    handler(event, {})
