import traceback

import event_poller


def handler(event, context):
    pollings = [
        event_poller.poll,
    ]
    errors = 0

    for poll in pollings:
        try:
            poll()
        except:
            # If one of the polling methods fails it should not stop the others from running.
            traceback.print_exc()
            errors += 1

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