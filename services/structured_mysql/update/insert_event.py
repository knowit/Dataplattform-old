import os
import pymysql
import json
from random import randint


class EventSQLs:
    def __init__(self, db_connection, db_events):
        self._db_connection = db_connection
        self._sql_queries = []

        self._event_ids_to_be_deleted = []
        self._new_event_codes_not_yet_committed = []
        self._active_event_codes_in_db = self._get_event_codes_in_db(db_events)
        self._event_button_name_id_mapping = self._get_event_button_name_id_mapping()

    def get_sql_queries(self):
        return self._sql_queries

    def append_insert_or_update_queries_from_event(self, event):
        parameters = self._parameters_from_event(event)
        event_insert_sqls = self._create_insert_sqls_for_all_event_boxes(parameters, event)
        self._sql_queries.extend(event_insert_sqls)

    def append_delete_queries_from_event(self, event):
        event_id = event['event_id']
        if event_id not in self._event_ids_to_be_deleted:
            delete_sql = f"DELETE FROM EventRatingType WHERE event_id = '{event_id}';"
            self._sql_queries.append(delete_sql)
            self._event_ids_to_be_deleted.append(event_id)

    def execute_sql_queries(self):
        for insert_sql in self._sql_queries:
            cursor = self._db_connection.cursor()
            try:
                cursor.execute(insert_sql)
            except pymysql.err.Error as e:
                print(f"Something went wrong with: {insert_sql}\n"
                      f"Error: {e}")

    def _get_event_codes_in_db(self, db_events):
        return [db_event['event_code'] for db_event in db_events]

    def _get_event_button_name_id_mapping(self):
        cursor = self._db_connection.cursor()
        get_event_buttons_sql = "SELECT event_button_id, event_button_name FROM EventBoxes;"
        try:
            cursor.execute(get_event_buttons_sql)
        except pymysql.err.Error as e:
            print(f"Something went wrong with: {str(get_event_buttons_sql)}. Error: {e}")

        event_buttons = cursor.fetchall()

        event_buttons_name_id_mapping = \
            {event_button['event_button_name']: event_button['event_button_id'] for event_button in event_buttons}
        return event_buttons_name_id_mapping

    def _parameters_from_event(self, event):
        parameters_from_event = ['id', 'event_button_id'] + list(event.keys())
        return parameters_from_event

    def _create_insert_sqls_for_all_event_boxes(self, parameters, event):
        parameters_string = ', '.join(parameters)
        event_replacement_attributes = {
            "id": str(event['event_id']),
            "event_button_id": 'NULL',
            "event_button_name": 'NULL'
        }

        event_boxes_for_event_left_to_check = event['event_button_name']

        insert_sql_queries = []
        while True:
            values = self._values_string_builder(parameters, event, event_replacement_attributes)
            values_string = ', '.join(values)

            parameters_equals_values = \
                [parameter + '=' + value for (parameter, value) in zip(parameters, values) if parameter != "id"]
            parameters_equals_values_string = ', '.join(parameters_equals_values)

            event_insert_sql = (f'INSERT IGNORE INTO EventRatingType ({parameters_string}) '
                                f'VALUES ({values_string}) '
                                f'ON DUPLICATE KEY UPDATE {parameters_equals_values_string};')

            insert_sql_queries.append(event_insert_sql)

            if len(event_boxes_for_event_left_to_check) == 0:
                break
            else:
                event_replacement_attributes['event_button_name'] = \
                    event_boxes_for_event_left_to_check.pop(0)
                event_replacement_attributes['event_button_id'] = \
                    self._event_button_name_id_mapping[event_replacement_attributes['event_button_name']]
                event_replacement_attributes['id'] = \
                    event_replacement_attributes['id'] + str(event_replacement_attributes['event_button_id'])

        return insert_sql_queries

    def _values_string_builder(self, parameters, event, event_replacement_attributes):
        values = []
        for parameter in parameters:
            if parameter == 'id':
                values.append(self.json_stringify(event_replacement_attributes['id']))
            elif parameter == 'event_button_id':
                values.append(self.json_stringify(event_replacement_attributes['event_button_id']))
            elif parameter == 'event_button_name':
                values.append(self.json_stringify(event_replacement_attributes['event_button_name']))
            else:
                values.append(self.json_stringify(event[parameter]))

        return values

    def json_stringify(self, element):
        return json.dumps(element, ensure_ascii=False)

    def generate_event_code(self):
        while True:
            generated_number = randint(0, 99999)
            padded_generated_number = str(generated_number).zfill(5)
            event_code = f'{padded_generated_number}'

            if event_code not in self._active_event_codes_in_db \
                    and event_code not in self._new_event_codes_not_yet_committed:
                self._new_event_codes_not_yet_committed.append(event_code)
                return event_code


def handler(event, context):
    db_connection = _get_db_connection()

    # google_events = _get_google_events(event)
    google_events = event["data"]
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
        print(google_event_id)
        print(db_event_ids)
        if google_event_id in db_event_ids:
            print("got in")
            db_event_code = [e['event_code'] for e in db_events if e['event_id'] == google_event_id].pop(0)
            google_event['event_code'] = db_event_code
        else:
            google_event['event_code'] = queries.generate_event_code()

        queries.append_insert_or_update_queries_from_event(google_event)

    # Execute sql queries so that db is in sync with google calendar
    for query in queries.get_sql_queries():
        print(query)
    queries.execute_sql_queries()
    db_connection.commit()
    db_connection.close()

    print("closed connection")

    return {
        'statusCode': 200,
        'body': 'Done'
    }


def _get_db_connection():
    return pymysql.connect(
        # host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        # port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        # user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        # password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        # db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        host="dataplattform-test-master.c7eijnq1j6fs.eu-central-1.rds.amazonaws.com",
        port=int("3306"),
        user="admin",
        password="dSMEMz5YIGCeK2q2ApvI",
        db="Dataplattform",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


def _get_google_events(event):
    google_events = {}
    for records in event['Records']:
        google_event = json.loads(records['Sns']['Message'])['data']
        google_events.update(google_event)

    return google_events


def _get_events_from_db_which_are_active_the_next_24_hours(db_connection):
    getSavedEventsSql = "SELECT id, event_id, event_button_id, active, event_code " \
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
    event = {"data": {
        "3mbuq0b4pciqef8qghu4ouc715": {"calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                                       "timestamp_from": 1575381600, "timestamp_to": 1575396000,
                                       "event_summary": "Rust kodekveld", "event_button_name": [],
                                       "creator": "thomas.tokje@knowit.no"},
        "5sp3pome607cff0pktahpve6pc": {"calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                                       "timestamp_from": 1575387900, "timestamp_to": 1575391500,
                                       "event_summary": "Speech training with Oslo Speaking Club",
                                       "event_button_name": [], "creator": "alina.kay@knowit.no"},
        "755fd38mdr0egjo8i5i6h2lt0l": {"calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                                       "timestamp_from": 1575554400, "timestamp_to": 1575561600,
                                       "event_summary": "3D-printerkveld", "event_button_name": [],
                                       "creator": "ab@knowit.no"},
        "6bu90333au1rks6sv6370t9qk6": {"calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                                       "timestamp_from": 1576076400, "timestamp_to": 1576083600,
                                       "event_summary": "Knowit Objectnet Mangekamp: Bowling", "event_button_name": [],
                                       "creator": "aulon.mujaj@knowit.no"},
        "06vllccjqsurk9t7jr695fdnai": {"calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                                       "timestamp_from": 1576191600, "timestamp_to": 1576278000,
                                       "event_summary": "Julebord", "event_button_name": ['alfa'],
                                       "creator": "marius.backer@knowit.no"}}}
    handler(event, {})
