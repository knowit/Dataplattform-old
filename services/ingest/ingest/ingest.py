import base64
import json
from ingest.ingest_util import IngestUtil
import ingest.filters as filters
import os
import urllib.request
import urllib.parse


update_types = {'EventRatingType', }


def handler(event, context):
	data_type = event["pathParameters"]["type"]
	data = event["body"]

	if type(data) is dict:
		data = json.dumps(data)

	if data_type in filters.filter:
		data = filters.filter[data_type](data)
	timestamp, timestamp_random = IngestUtil.insert_doc(data_type, data=data)

	if data_type in update_types:
		post_to_update(data_type, data)

	return {
		'statusCode': 200,
		'body': json.dumps({
			"timestamp": timestamp,
			"id": base64.b64encode(timestamp_random).decode("utf-8")
		})
	}


def post_to_update(data_type, body):
	url = os.getenv("DATAPLATTFORM_UPDATE_URL")
	apikey = os.getenv("DATAPLATTFORM_UPDATE_APIKEY")

	data = body.encode("ascii")

	url += data_type
	try:
		request = urllib.request.Request(url, data=data, headers={"x-api-key": apikey})
		response = urllib.request.urlopen(request)
		return response.getcode()
	except urllib.request.HTTPError:
		return 500
