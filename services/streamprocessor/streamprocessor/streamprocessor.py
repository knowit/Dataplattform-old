import json


def handler(event, context):
    print("-------------------")
    try:
        #1 Iterate over each record
        for record in event['Records']:
            #2 handle event type
            if record['eventName'] == 'INSERT':
                handle_insert(record)
            else:
                continue

    except Exception as e:
        print(e)
        return "Oops!"

def handle_insert(record):
    #handling insert

    newImage = record['dynamodb']['NewImage']
    #parse
    print("new row added")
    print(newImage)






