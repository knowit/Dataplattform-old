import json
from random import randint
import pymysql


class DeleteEventSQLs:
    def __init__(self, db_connection):
        self._db_connection_cursor = db_connection.cursor()
        self._delete_sqls = []

    def append(self, event):
        event_id = event['id']
        delete_sql = f"DELETE FROM EventRatingType WHERE id = '{event_id}';"
        self._delete_sqls.append(delete_sql)

    def execute_sqls(self):
        for delete_sql in self._delete_sqls:
            try:
                self._db_connection_cursor.execute(delete_sql)
            except pymysql.err.IntegrityError:
                print(f'Something went wrong with: {str(delete_sql)}')


class InsertEventSQLs:
    def __init__(self, db_connection, db_events):
        self._db_connection_cursor = db_connection.cursor()
        self._insert_sqls = []
        self._new_event_codes_not_yet_commited = []
        self._active_event_codes_in_db = [db_event['event_code'] for db_event in db_events if db_event['active']]
        self._event_button_name_id_mapping = self._get_event_button_name_id_mapping()

    def append(self, event):
        parameters = self._parameter_string_builder(event)
        event_insert_sqls = self._create_insert_sqls_for_all_event_boxes(parameters, event)
        self._insert_sqls.extend(event_insert_sqls)

    def execute_sqls(self):
        for insert_sql in self._insert_sqls:
            try:
                self._db_connection_cursor.execute(insert_sql)
            except pymysql.err.IntegrityError:
                print(f'Something went wrong with: {str(insert_sql)}')

    def _get_event_button_name_id_mapping(self):
        sql = "SELECT event_button_id, event_button_name FROM EventBoxes;"
        try:
            self._db_connection_cursor.execute(sql)
        except pymysql.err.IntegrityError:
            print("Something went wrong getting EventBoxes.")

        event_buttons = self._db_connection_cursor.fetchall()
        event_buttons_name_id_mapping = \
            {event_button['event_button_name']: event_button['event_button_id'] for event_button in event_buttons}
        return event_buttons_name_id_mapping

    def _parameter_string_builder(self, event):
        parameters = [parameter for parameter in (['id', 'event_id'] + event)]

        parameters_string = ', '.join(parameters)
        return parameters_string

    def _create_insert_sqls_for_all_event_boxes(self, parameters, event):
        event_id = event['id']
        event_button_id = 'NULL'
        event_button_name = 'NULL'

        event_boxes_for_event_left_to_check = event['event_button_name']

        insert_sqls = []
        while True:
            values = self._values_string_builder(event, event_id, event_button_id, event_button_name)
            parameters_equals_values = [parameter + "=" + value for (parameter, value) in zip(parameters, values)]
            parameters_equals_values_string = ", ".join(parameters_equals_values)

            event_insert_sql = (f"INSERT IGNORE INTO EventRatingType({parameters}) "
                                f"VALUES ({values}) "
                                f"ON DUPLICATE KEY UPDATE {parameters_equals_values_string};")

            insert_sqls.append(event_insert_sql)

            if len(event_boxes_for_event_left_to_check) == 0:
                break
            else:
                event_button_name = event_boxes_for_event_left_to_check.pop(0)
                event_button_id = self._event_button_name_id_mapping[event_button_name]
                event_id = event['id'] + event_button_id

        return insert_sqls

    def _values_string_builder(self, event, event_id, event_button_id, event_button_name):
        values = []
        for parameter in event:
            if parameter == 'event_id':
                values.append(event_id)
            if parameter == 'event_code':
                values.append(self._generate_event_code())
            if parameter == 'event_button_id':
                values.append(event_button_id)
            if parameter == 'event_button_name':
                values.append(event_button_name)
            else:
                values.append(json.dumps(event[parameter], ensure_ascii=False))

        values_string = ', '.join(values)
        return values

    def _generate_event_code(self):
        while True:
            generated_event_code_number = randint(0, 99999)
            padded_generated_event_code_number = str(generated_event_code_number).zfill(5)

            if padded_generated_event_code_number not in self._active_event_codes_in_db \
                    and padded_generated_event_code_number not in self._new_event_codes_not_yet_commited:
                self._new_event_codes_not_yet_commited.append(padded_generated_event_code_number)
                return padded_generated_event_code_number
