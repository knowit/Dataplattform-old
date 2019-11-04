import json
import pymysql
import pandas as pd
from .database_connection import get_connection

def load_graph(data_dict, path):
	graph = json.load(open(path, encoding='utf-8'))
	del graph['layout']['template']['themeRef']

	for jsonData in graph['data']:
		for column in jsonData['meta']['columnNames']:
			if jsonData['name'] not in data_dict:
				raise ValueError(
					"{:d} does not exist in input dictionary".format(
						jsonData['name']
					)
				)
			if column in data_dict[jsonData['name']]:
				jsonData[column] = data_dict[jsonData['name']][column]


	return graph


def get_data(sql):
	
	connection = get_connection()
	data = pd.read_sql(sql, connection)
	connection.close()
	return data
