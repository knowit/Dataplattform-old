import traceback

import event_poller


def handler(event, context):
    pollings = [
        event_poller.poll,
    ]
    errors = 0

    for poll in pollings:
        print("//////////////////POLLING//////////////////////////")
        poll()

    if errors == 0:
        return {
            'statusCode': 200,
            'body': 'Done'
        }

    else:
        return {
            'statusCode': 500,
            'body': 'Error'
        }