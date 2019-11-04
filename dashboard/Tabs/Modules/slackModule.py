from .abstractModule import abstractModule
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import os
from .Utils.utils import load_graph, get_data

class SlackModule(abstractModule):

	sql_query_messages = 'SELECT from_unixtime(slack_timestamp, "%Y-%m-%d") as dato, COUNT(*) as messages FROM Dataplattform.SlackType GROUP BY dato ORDER BY slack_timestamp desc;'
	sql_query_reactions = 'SELECT from_unixtime(slack_timestamp, "%Y-%m-%d") as dato, COUNT(*) as reactions FROM Dataplattform.SlackEmojiType WHERE event_type = "reaction_added" GROUP BY dato ORDER BY slack_timestamp desc;'


	def __init__(self):
		
		df_messages = get_data(self.sql_query_messages)
		df_reactions = get_data(self.sql_query_reactions)

		data = {
			"Reactions":{
				"y": df_reactions.reactions.tolist(),
				"x": df_reactions.dato.tolist(),
			},
			"Messages":{
				"y": df_messages.messages.tolist(),
				"x": df_messages.dato.tolist(),
			},
		}

		path = os.path.dirname(__file__) + "/Graphs/SlackActivity.json"
		graph = load_graph(data, path)
		fig = go.Figure(data=graph['data'], layout=graph['layout'])

		self.dccGraph = dcc.Graph(figure=fig, style=self.graph_style)


	def get_module(self):
		return self.dccGraph


