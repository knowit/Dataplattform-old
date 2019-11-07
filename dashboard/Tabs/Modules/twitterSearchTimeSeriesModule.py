from .abstractModule import abstractModule
import dash_core_components as dcc
import pandas as pd
from .Utils.utils import get_data
from .Graphs.Trace import Trace
from .Graphs.Trace import Bar

class TwitterSearchTimeSeriesModule(abstractModule):
    sql_query = "SELECT created " \
                "FROM Dataplattform.TwitterSearchType " \

    def __init__(self):

        df = get_data(self.sql_query)
        df = self.prepare_data(df)

        fig = Trace(
            df, data_layout=[["created", "posts"]],
            title="Tweets omhandlet Knowit", axis_text=["Dato", "Tweets"],
            axis_type=["date", "linear"], show_legend=False, line_fill="tonexty")

        self.dccGraph = dcc.Graph(figure=fig.get_trace(), style=self.graph_style)


    def get_module(self):
        return self.dccGraph


    def prepare_data(self, data):
        data['created'] = pd.to_datetime(data['created'])
        data = data.set_index(data['created'])
        data['posts'] = 1
        data = data.resample('M').sum()
        data['created'] = data.index
        return data
