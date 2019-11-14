import datetime
import os
import googleapiclient.discovery
import json
import urllib.request
import urllib.parse
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import boto3


def poll():
    creds_file = 'creds.json'
    if not os.path.exists(creds_file):
        print("No creds file")

    calendar_ids = os.getenv("DATAPLATTFORM_GOOGLE_CALENDAR_IDS").split(',')

    events = {
        "data": {}
    }

    for calendar_id in calendar_ids:
        events['data'].update(get_events(creds_file, calendar_id))

    url = os.getenv("DATAPLATTFORM_INSERT_URL")
    insert_key = os.getenv("DATAPLATTFORM_INSERT_APIKEY")
    data = json.dumps(events)

    sns = boto3.client('sns')

    response = sns.publish(
        TopicArn=os.getenv("DATAPLATTFORM_PUBLISH_EVENT"),
        Message=data
    )

    print("////////////////////////////////RESPONSE//////////////////////////////")
    print(response)

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
    now = datetime.datetime.utcnow().isoformat() + '+02:00'
    tomorrow = datetime.datetime.utcfromtimestamp(datetime.datetime.now().timestamp()
                                                  + (60 * 60 * 24)).isoformat() + '+02:00'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        timeMax=tomorrow,
        timeZone='UTC+0:00',
        singleEvents=True,
        orderBy='startTime') \
        .execute()
    events = events_result.get('items', [])
    info = {}
    for event in events:
        boxes = []
        if 'location' in event:
            temp = event['location'].split(',')
            for box in temp:
                if "Enheter" in box:
                    boxes.append(box.split('-')[-1])

        startTime = ""
        endTime = 0
        if "dateTime" in event['start']:
            startTime = get_timestamp(event['start']['dateTime'])
        else:
            timeObject = list(map(int, event['start']['date'].split("-")))
            startTime = datetime.datetime.timestamp(datetime.datetime(timeObject[0], timeObject[1], timeObject[2]))
        if "dateTime" in event['end']:
            endTime = get_timestamp(event['end']['dateTime'])
        else:
            timeObject = list(map(int, event['end']['date'].split("-")))
            endTime = datetime.datetime.timestamp(datetime.datetime(timeObject[0], timeObject[1], timeObject[2]))

        summary = ""
        if "summary" in event:
            summary = event["summary"]

        creator = ""
        if "creator" in event:
            creator = event['creator']['email']

        info[event['id']] = {
            'calendar_id': calendar_id,
            'timestamp_from': startTime,
            'timestamp_to': endTime,
            'event_summary': summary,
            'event_button_name': boxes,
            'creator': creator,
        }
    return info


def get_timestamp(date):
    date = date.split('T')
    date_array = list(map(int, date[0].split('-')))
    time_array = list(map(int, date[1].split('Z')[0].split(':')))
    date_start = datetime.datetime(date_array[0], date_array[1], date_array[2],
                                   time_array[0], time_array[1], time_array[2])
    return datetime.datetime.timestamp(date_start)
