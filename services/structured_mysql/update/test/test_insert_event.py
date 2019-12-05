import os
import pymysql
import json
from typing import Dict, Union, List
import pytest
import insert_event
import insert_event_util
import re


class TestInsertEvent:
    @pytest.fixture
    def db_events(self):
        db_events = [
            {'id': '3mbuq0b4pciqef8qghu4ouc715', 'event_id': '3mbuq0b4pciqef8qghu4ouc715', 'event_button_id': 0,
             'event_code': '01096'},
            {'id': '5sp3pome607cff0pktahpve6pc', 'event_id': '5sp3pome607cff0pktahpve6pc', 'event_button_id': 0,
             'event_code': '07653'}]
        return db_events

    @pytest.fixture
    def db_connection(self):
        class DBConnectionMock:
            def connect(self, **kvarg):
                pass

            def commit(self):
                pass

            def close(self):
                pass

            def cursor(self):
                class DBCursorMock:
                    def execute(self, query):
                        pass

                    def fetchall(self):
                        return []

                return DBCursorMock()

        return DBConnectionMock()

    @pytest.fixture
    def event(self):
        event = {
            "Records": [{
                "Sns": {
                    "Message": json.dumps({
                        "data": {
                            "3mbuq0b4pciqef8qghu4ouc715": {
                                "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                                "timestamp_from": 1575381600, "timestamp_to": 1575396000,
                                "event_summary": "Rust kodekveld", "event_button_names": [],
                                "creator": "thomas.tokje@knowit.no"},
                            "5sp3pome607cff0pktahpve6pc": {
                                "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                                "timestamp_from": 1575387900, "timestamp_to": 1575391500,
                                "event_summary": "Speech training with Oslo Speaking Club",
                                "event_button_names": [], "creator": "alina.kay@knowit.no"},
                            "755fd38mdr0egjo8i5i6h2lt0l": {
                                "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                                "timestamp_from": 1575554400, "timestamp_to": 1575561600,
                                "event_summary": "3D-printerkveld", "event_button_names": [],
                                "creator": "ab@knowit.no"},
                            "6bu90333au1rks6sv6370t9qk6": {
                                "calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                                "timestamp_from": 1576076400, "timestamp_to": 1576083600,
                                "event_summary": "Knowit Objectnet Mangekamp: Bowling", "event_button_names": [],
                                "creator": "aulon.mujaj@knowit.no"},
                            "06vllccjqsurk9t7jr695fdnai": {
                                "calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                                "timestamp_from": 1576191600, "timestamp_to": 1576278000,
                                "event_summary": "Julebord", "event_button_names": ['alfa'],
                                "creator": "marius.backer@knowit.no"}
                        }
                    })
                }
            }
            ]
        }

        return event

    @pytest.fixture
    def google_events(self):
        google_events = {
            "3mbuq0b4pciqef8qghu4ouc715": {
                "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                "timestamp_from": 1575381600, "timestamp_to": 1575396000,
                "event_summary": "Rust kodekveld", "event_button_names": [],
                "creator": "thomas.tokje@knowit.no"},
            "5sp3pome607cff0pktahpve6pc": {
                "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                "timestamp_from": 1575387900, "timestamp_to": 1575391500,
                "event_summary": "Speech training with Oslo Speaking Club",
                "event_button_names": [], "creator": "alina.kay@knowit.no"},
            "755fd38mdr0egjo8i5i6h2lt0l": {
                "calendar_id": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                "timestamp_from": 1575554400, "timestamp_to": 1575561600,
                "event_summary": "3D-printerkveld", "event_button_names": [],
                "creator": "ab@knowit.no"},
            "6bu90333au1rks6sv6370t9qk6": {
                "calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                "timestamp_from": 1576076400, "timestamp_to": 1576083600,
                "event_summary": "Knowit Objectnet Mangekamp: Bowling", "event_button_names": [],
                "creator": "aulon.mujaj@knowit.no"},
            "06vllccjqsurk9t7jr695fdnai": {
                "calendar_id": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com",
                "timestamp_from": 1576191600, "timestamp_to": 1576278000,
                "event_summary": "Julebord", "event_button_names": ['alfa'],
                "creator": "marius.backer@knowit.no"}
        }

        return google_events

    @pytest.fixture
    def event_boxes_mapping(self):
        event_buttons = [{'event_button_id': 19625, 'event_button_name': 'alfa'},
                         {'event_button_id': 55331, 'event_button_name': 'bravo'},
                         {'event_button_id': 24602, 'event_button_name': 'charlie'}]
        event_buttons_name_id_mapping = \
            {event_button['event_button_name']: event_button['event_button_id'] for event_button in event_buttons}
        return event_buttons_name_id_mapping

    def test_get_google_events(self, event, google_events):
        assert google_events == insert_event.get_google_events(event)

    class TestHandler:

        @pytest.fixture(autouse=True)
        def setup(self, monkeypatch, db_connection, event_boxes_mapping):
            monkeypatch.setattr(insert_event, 'get_db_connection', (lambda: db_connection))
            monkeypatch.setattr(insert_event_util.EventQueries, '_get_event_button_name_id_mapping',
                                (lambda _: event_boxes_mapping))

        def remove_occurences_of_event_code_from_query(self, string):
            string = re.sub(r'event_code="[0-9]{5}"', 'event_code="', string)
            string = re.sub(r'"[0-9]{5}"\) ON DUPLICATE KEY UPDATE', '"") ON DUPLICATE KEY UPDATE', string)
            return string

        def test_insert_of_google_event(self, monkeypatch, google_events, event, event_boxes_mapping):
            one_google_event = {"3mbuq0b4pciqef8qghu4ouc715": google_events["3mbuq0b4pciqef8qghu4ouc715"]}
            monkeypatch.setattr(insert_event, 'get_google_events', (lambda _: one_google_event))
            monkeypatch.setattr(insert_event, 'get_events_from_db_which_are_active_the_next_24_hours',
                                (lambda e: []))

            def execute_sql_queries_stub(s: insert_event_util.EventQueries):
                real_list_of_queries = s.get_sql_queries()
                test_list_of_queries = [
                    ('INSERT IGNORE INTO EventRatingType (id, event_button_id, event_button_name, '
                     'calendar_id, timestamp_from, timestamp_to, event_summary, creator, event_id, event_code) '
                     'VALUES ("3mbuq0b4pciqef8qghu4ouc715", "NULL", "NULL", '
                     '"knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com", '
                     '1575381600, 1575396000, "Rust kodekveld", "thomas.tokje@knowit.no", '
                     '"3mbuq0b4pciqef8qghu4ouc715", "41026") ON DUPLICATE KEY UPDATE event_button_id="NULL", '
                     'event_button_name="NULL", '
                     'calendar_id="knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com", '
                     'timestamp_from=1575381600, timestamp_to=1575396000, event_summary="Rust kodekveld", '
                     'creator="thomas.tokje@knowit.no", event_id="3mbuq0b4pciqef8qghu4ouc715", event_code="41026";')]

                for (real, test) in zip(real_list_of_queries, test_list_of_queries):
                    # Test that they are equal without event code since this is a random code
                    assert self.remove_occurences_of_event_code_from_query(real) == \
                           self.remove_occurences_of_event_code_from_query(test)

            monkeypatch.setattr(insert_event_util.EventQueries, 'execute_sql_queries', execute_sql_queries_stub)
            monkeypatch.setattr(insert_event_util.EventQueries, '_get_event_button_name_id_mapping',
                                (lambda _: event_boxes_mapping))

            insert_event.handler(event, {})

        def test_update_if_google_event_already_in_db(self, monkeypatch, event, google_events, db_events):
            list_with_one_google_event = {"3mbuq0b4pciqef8qghu4ouc715": google_events["3mbuq0b4pciqef8qghu4ouc715"]}
            monkeypatch.setattr(insert_event, 'get_google_events', (lambda _: list_with_one_google_event))

            list_with_one_db_event = \
                [db_event for db_event in db_events if db_event['id'] == "3mbuq0b4pciqef8qghu4ouc715"]
            monkeypatch.setattr(insert_event, 'get_events_from_db_which_are_active_the_next_24_hours',
                                (lambda e: list_with_one_db_event))

            def execute_sql_queries_stub(s: insert_event_util.EventQueries):
                real_list_of_queries = s.get_sql_queries()
                test_list_of_queries = [
                    'INSERT IGNORE INTO EventRatingType (id, event_button_id, event_button_name, '
                    'calendar_id, timestamp_from, timestamp_to, event_summary, creator, event_id, event_code) '
                    'VALUES ("3mbuq0b4pciqef8qghu4ouc715", "NULL", "NULL", '
                    '"knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com", 1575381600, 1575396000, '
                    '"Rust kodekveld", "thomas.tokje@knowit.no", "3mbuq0b4pciqef8qghu4ouc715", "01096") '
                    'ON DUPLICATE KEY UPDATE event_button_id="NULL", event_button_name="NULL", '
                    'calendar_id="knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com", '
                    'timestamp_from=1575381600, timestamp_to=1575396000, event_summary="Rust kodekveld", '
                    'creator="thomas.tokje@knowit.no", event_id="3mbuq0b4pciqef8qghu4ouc715", event_code="01096";']

                for (real, test) in zip(real_list_of_queries, test_list_of_queries):
                    assert real == test

            monkeypatch.setattr(insert_event_util.EventQueries, 'execute_sql_queries', execute_sql_queries_stub)
            insert_event.handler(event, {})

        def test_delete_from_db_if_google_events_no_longer_has_event(self, monkeypatch, event, db_events):
            monkeypatch.setattr(insert_event, 'get_google_events', (lambda _: {}))

            list_with_one_db_event = \
                [db_event for db_event in db_events if db_event['id'] == "3mbuq0b4pciqef8qghu4ouc715"]
            monkeypatch.setattr(insert_event, 'get_events_from_db_which_are_active_the_next_24_hours',
                                (lambda e: list_with_one_db_event))

            def execute_sql_queries_stub(s: insert_event_util.EventQueries):
                real_list_of_queries = s.get_sql_queries()
                test_list_of_queries = ["DELETE FROM EventRatingType WHERE event_id = '3mbuq0b4pciqef8qghu4ouc715';"]

                for (real, test) in zip(real_list_of_queries, test_list_of_queries):
                    assert real == test

            monkeypatch.setattr(insert_event_util.EventQueries, 'execute_sql_queries', execute_sql_queries_stub)
            insert_event.handler(event, {})
