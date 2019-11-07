import json
import pymysql
import pandas as pd
from .database_connection import get_connection

def load_graph(data_dict, path):
	graph = json.load(open(path, encoding='utf-8'))
	del graph['layout']['template']['themeRef']

	for jsonData in graph['data']:
		update_graph(jsonData, data_dict)


	return graph


def update_graph(jsonData, data_dict):
	if jsonData['name'] not in data_dict:
				raise ValueError(
					"{:d} does not exist in input dictionary".format(
						jsonData['name']
					)
				)
	for column in jsonData['meta']['columnNames']:
		if isinstance(jsonData['meta']['columnNames'][column], str):
			if jsonData['meta']['columnNames'][column] in data_dict[jsonData['name']]:
				jsonData[column] = data_dict[jsonData['name']][jsonData['meta']['columnNames'][column]]
		elif isinstance(jsonData['meta']['columnNames'][column], dict):
			for subColumn in jsonData['meta']['columnNames'][column]:
				if jsonData['meta']['columnNames'][column][subColumn] in data_dict[jsonData['name']][column]:
					jsonData[column][subColumn] = data_dict[jsonData['name']][column][jsonData['meta']['columnNames'][column][subColumn]]
			del  jsonData[column]['meta']


def get_data(sql, params=None):
	
	connection = get_connection()
	if params:
		data = pd.read_sql(sql, connection, params=params)
	else:
		data = pd.read_sql(sql, connection)

	connection.close()
	return data
