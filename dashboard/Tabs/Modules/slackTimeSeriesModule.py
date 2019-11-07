from .abstractModule import abstractModule
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import os
from .Utils.utils import load_graph, get_data
from .Graphs.Trace import Trace

class SlackModule(abstractModule):

	sql_query_messages = 'SELECT from_unixtime(slack_timestamp, "%Y-%m-%d") as dato, COUNT(*) as messages FROM Dataplattform.SlackType GROUP BY dato ORDER BY slack_timestamp desc;'
	sql_query_reactions = 'SELECT from_unixtime(slack_timestamp, "%Y-%m-%d") as dato, COUNT(*) as reactions FROM Dataplattform.SlackEmojiType WHERE event_type = "reaction_added" GROUP BY dato ORDER BY slack_timestamp desc;'


	def __init__(self):
		
		df = get_data(self.sql_query_messages).merge(get_data(self.sql_query_reactions), on="dato", how="outer")

		fig = Trace(
			df, data_layout=[["dato", "reactions"], ["dato", "messages"]], 
			axis_type=["date", "linear"], title="Aktivitetsnivå på Slack", 
			axis_text=["Tid", "Antall"], names=["Reactions", "Messages"])

		self.dccGraph = dcc.Graph(figure=fig.get_trace(), style=self.graph_style)


	def get_module(self):
		return self.dccGraph



class Slack3DGraph(abstractModule):

	sql_query = 'SELECT positive_ratio, neutral_ratio, negative_ratio, COUNT(*) as antall, reaction FROM Dataplattform.SlackEmojiType WHERE positive_ratio IS NOT NULL AND date(from_unixtime(slack_timestamp)) = curdate() GROUP BY reaction;'


	def __init__(self):
		rawData = get_data(self.sql_query)

		data = {
			"Test": {
				"neutral": rawData.neutral_ratio.tolist(),
				"negative": rawData.negative_ratio.tolist(),
				"positive": rawData.positive_ratio.tolist(),
				"reaction": rawData.reaction.tolist(),
				"marker": {
					"antall": rawData.antall.tolist(),
				}
			}
		}

		path = os.path.dirname(__file__) + "/Graphs/slackStemning.json"
		graph = load_graph(data, path)
		fig = go.Figure(data=graph['data'], layout=graph['layout'])

		self.dccGraph = dcc.Graph(figure=fig, style=self.graph_style)


	def get_module(self):
		return self.dccGraph
