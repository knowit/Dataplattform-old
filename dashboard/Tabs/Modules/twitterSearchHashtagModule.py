from .abstractModule import abstractModule
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import os
from .Utils.utils import load_graph, get_data
from .Graphs.Trace import Trace
from .Graphs.Trace import Bar

class TwitterSearchHashtagModule(abstractModule):

    sql_query = "SELECT created, hashtags " \
                "FROM Dataplattform.TwitterSearchType " \
                "WHERE hashtags <> ''" \

    def __init__(self):

        df = get_data(self.sql_query)
        df = self.prepare_data(df)

        fig = Bar(
            df, data_layout=[["freq", "hashtag"]],
            title="Mest brukte emneknagger", axis_text=["Antall", "Emneknagg"],
            names=["Emneknagg"], orientation="h", show_legend=False, show_yaxis_text=False)

        self.dccGraph = dcc.Graph(figure=fig.get_trace(), style=self.graph_style)


    def get_module(self):
        return self.dccGraph


    def prepare_data(self, data):
        word_freq = {}

        for hashtags in data['hashtags']:
            words = hashtags.split()
            for word in words:
                if word == "#":
                    continue

                word = word.lower()
                if not word.startswith('#'):
                    word = '#' + word

                if word not in word_freq.keys():
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

        freq = pd.DataFrame()
        freq['hashtag'] = word_freq.keys()
        freq['freq'] = word_freq.values()
        freq = freq.sort_values(by=['freq'])
        return freq[-10:]




