from insert_event_util import EventQueries, get_db_connection, get_google_events, \
    get_events_from_db_which_are_active_the_next_24_hours
from typing import Dict, Union, List

db_connection = None


def handler(event: Dict, context) -> Dict[str, Union[str, int]]:
    global db_connection
    if db_connection is None:
        db_connection = get_db_connection()

    google_events = get_google_events(event)
    db_events = get_events_from_db_which_are_active_the_next_24_hours(db_connection)

    queries = EventQueries(db_connection, db_events)

    # Construct DELETE queries for deleted google events from db or single DELETE queries if an event button is removed
    google_event_ids = list(google_events.keys()) if len(google_events) > 0 else []
    for db_event in db_events:
        if db_event['event_id'] not in google_event_ids:
            queries.append_delete_queries_from_event(db_event)
        elif db_event['event_id'] in google_event_ids and db_event['event_button_name'] != 'NULL' and \
                not EventQueries.is_event_button_still_in_google_event(db_event, google_events[
                    db_event['event_id']]):
            queries.append_single_delete_query_from_event(db_event)

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
