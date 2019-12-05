import pytest
import json
from insert_event_util import EventQueries


class TestInsertEventUtil:

    @pytest.fixture
    def db_connection(self):
        class DBConnectionMock:
            def connect(self, **kvarg):
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
    def db_events(self):
        db_events = [
            {'id': '3mbuq0b4pciqef8qghu4ouc715', 'event_id': '3mbuq0b4pciqef8qghu4ouc715', 'event_button_id': 0,
             'event_code': '01096'},
            {'id': '5sp3pome607cff0pktahpve6pc', 'event_id': '5sp3pome607cff0pktahpve6pc', 'event_button_id': 0,
             'event_code': '07653'}]
        return db_events

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

    def test_generate_event_code(self, monkeypatch, db_connection):
        event_queries = EventQueries(db_connection, [])
        generated_event_code = event_queries.generate_event_code()
        assert len(generated_event_code) == 5

    def test_append_insert_or_update_queries_from_event(self, monkeypatch, db_connection, google_events):
        event_queries = EventQueries(db_connection, [])
        event = google_events["3mbuq0b4pciqef8qghu4ouc715"]
        event['event_code'] = '12345'
        event['event_id'] = 'fake_event_id'
        event_queries.append_insert_or_update_queries_from_event(event)
        real = event_queries.get_sql_queries()
        test = [
            'INSERT IGNORE INTO EventRatingType (id, event_button_id, event_button_name, calendar_id, '
            'timestamp_from, timestamp_to, event_summary, creator, event_code, event_id) VALUES ("fake_event_id", '
            '"NULL", "NULL", "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com", 1575381600, 1575396000, '
            '"Rust kodekveld", "thomas.tokje@knowit.no", "12345", "fake_event_id") '
            'ON DUPLICATE KEY UPDATE event_button_id="NULL", event_button_name="NULL", '
            'calendar_id="knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com", timestamp_from=1575381600, '
            'timestamp_to=1575396000, event_summary="Rust kodekveld", creator="thomas.tokje@knowit.no", '
            'event_code="12345", event_id="fake_event_id";'
        ]
        assert real == test

    def test_append_delete_queries_from_event(self, monkeypatch, db_connection, db_events):
        event_queries = EventQueries(db_connection, [])
        event = db_events[0]
        event_queries.append_delete_queries_from_event(event)
        assert event_queries.get_sql_queries() == ["DELETE FROM EventRatingType WHERE event_id = '3mbuq0b4pciqef8qghu4ouc715';"]
