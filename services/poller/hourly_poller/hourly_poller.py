import datetime
import json
import os
import traceback
import urllib

import googleapiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

import event_poller


def handler(event, context):
    pollings = [
        event_poller.poll,
    ]
    errors = 0

    poll()

    # for poll in pollings:
    #     try:
    #         prints += "Polling, "
    #         prints += poll(prints)
    #     except:
    #         prints += "Error!, "
    #         # If one of the polling methods fails it should not stop the others from running.
    #         traceback.print_exc()
    #         errors += 1
#
    if errors == 0:
        return {
            'statusCode': 200,
            'body': 'Done'
        }

    else:
        return {
            'statusCode': 500,
            'body': ''
        }


def poll():
    creds_file = 'creds.json'
    if not os.path.exists(creds_file):
        print("No creds file")

    calendar_ids = ["knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
                    "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com"]

    events = {
        "data": {}
    }

    for calendar_id in calendar_ids:
        events['data'].update(get_events(creds_file, calendar_id))

    url = os.getenv("DATAPLATTFORM_INSERT_URL")
    insert_key = os.getenv("DATAPLATTFORM_INSERT_APIKEY")
    data = json.dumps(events).encode("ascii")
    try:
        req = urllib.request.Request(url, headers={"x-api-key": insert_key}, data=data)
        response = urllib.request.urlopen(req)
    except:
        print("Error")
        return False

    return True


def get_events(credsfile, calendar_id):
    """
    :param creds: credentials
    :param calendar_id:
    :return: A dictionary containing (max 10) of the events in the nearest future from this
    specific calendar_id.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credsfile, [
        'https://www.googleapis.com/auth/calendar.readonly'])

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = googleapiclient.discovery.build(serviceName='calendar', version='v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    tomorrow = datetime.datetime.utcfromtimestamp(datetime.datetime.now().timestamp()
                                                  + (60 * 60 * 24)).isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        timeMax=tomorrow,
        singleEvents=True,
        orderBy='startTime') \
        .execute()
    events = events_result.get('items', [])
    info = {}
    for event in events:
        if 'location' in event:
            boxes = []
            temp = event['location'].split(',')
            for box in temp:
                if "Enheter" in box:
                    boxes.append(box.split('-')[-1])
            if len(boxes) > 0:
                info[event['id']] = {
                    'timestamp_from': get_timestamp(event['start']['dateTime']),
                    'timestamp_to': get_timestamp(event['end']['dateTime']),
                    'event_summary': event['summary'],
                    'event_button_name': boxes,
                    'creator': event['creator']['email'],
                }
    return info


def get_timestamp(date):
    date = date.split('T')
    date_array = list(map(int, date[0].split('-')))
    time_array = list(map(int, date[1].split('+')[0].split(':')))
    date_start = datetime.datetime(date_array[0], date_array[1], date_array[2],
                                   time_array[0], time_array[1], time_array[2])
    return datetime.datetime.timestamp(date_start)