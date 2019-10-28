import pymysql

def check_none(event):
    if not event['positive_count']:
        event['positive_count'] = 0
    if not event['neutral_count']:
        event['neutral_count'] = 0
    if not event['negative_count']:
        event['negative_count'] = 0
    return event

def summarize_events(events):
    new_events = []
    added_events = {}
    all_events = {'positive_count': 0, 'neutral_count': 0, 'negative_count': 0}


    for event in events:
        event = check_none(event)
        all_events['positive_count'] += event['positive_count']
        all_events['neutral_count'] += event['neutral_count']
        all_events['negative_count'] += event['negative_count']

        for event2 in events:
            event2 = check_none(event2)
            if event['event_id'] == event2['event_id']:
                if event['id'] != event2['id']:
                    event['positive_count'] += event2['positive_count']
                    event['neutral_count'] += event2['neutral_count']
                    event['negative_count'] += event2['negative_count']

        if event['event_id'] not in added_events:
            new_events.append(event)
            added_events[event['event_id']] = True

    return new_events, all_events


def get_data(type):
    print("fetching data")

    connection = connect_to_aurora_local()
    cur = connection.cursor()

    sql_query = ""

    try:
       response = cur.execute(sql_query)
    except pymysql.err.Error:
       cur.close()
       return None
    cur.close()

    events = summarize_events(cur.fetchall())
    return events



def remove_duplicates(events):
    new_events = []
    added_events = {}
    for event in events:
        if event['event_id'] not in added_events:
            new_events.append(event)
            added_events[event['event_id']] = True
    return new_events

def get_all_events():
    print("fetching data")

    connection = connect_to_aurora_local()
    cur = connection.cursor()

    sql_query = ""

    try:
        response = cur.execute(sql_query)
    except pymysql.err.Error:
        cur.close()
        return None
    cur.close()

    events = remove_duplicates(cur.fetchall())
    return events


def connect_to_aurora_local():
    return pymysql.connect(
        host="",
        port=0,
        user="",
        password="",
        db="",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


