from typing import Dict, Union
from web_api.events.events_service import patch_event, get_events


def handler(event, context) -> Dict[str, Union[int, str]]:
    if event['method'] == "GET":
        pass
    if event['method'] == "POST":
        pass
    if event['method'] == "PATCH":
        return patch_event(event)
    if event['method'] == "PUT":
        pass
    if event['method'] == "DELETE":
        pass
