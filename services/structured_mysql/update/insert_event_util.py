import json
from random import randint
import pymysql


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
