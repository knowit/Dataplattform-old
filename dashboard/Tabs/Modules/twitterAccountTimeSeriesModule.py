from .abstractModule import abstractModule
import dash_core_components as dcc
import pandas as pd
from .Utils.utils import get_data
from .Graphs.Trace import Trace
from .Graphs.Trace import Bar

class TwitterAccountTimeSeriesModule(abstractModule):
    sql_query = "SELECT created, user_screen_name " \
                "FROM Dataplattform.TwitterAccountType " \

    def __init__(self):

        df = get_data(self.sql_query)
        df = self.prepare_data(df)

        fig = Trace(
            df, data_layout=[["created", "all"],["created", "knowitab"],
                             ["created", "knowitnorge"], ["created", "knowitx"]],
            title="Tweets fra Knowit kontoer", axis_text=["Dato", "Tweets"],
            names=["Alle", "Knowit AB", "Knowit Norge", "Knowit Experience"],
            axis_type=["date", "linear"], show_legend=True, line_fill=["tonexty", 0])

        self.dccGraph = dcc.Graph(figure=fig.get_trace(), style=self.graph_style)

    def get_module(self):
        return self.dccGraph


    def prepare_data(self, data):
        accounts = {
            "knowitab",
            "knowitnorge",
            "knowitx"
        }

        data['created'] = pd.to_datetime(data['created'])
        data = data.set_index(data['created'])

        for account in accounts:
            data[account] = 0
            data.loc[data.user_screen_name == account, account] = 1

        data['all'] = 1
        data = data.resample('M').sum()
        data['created'] = data.index
        return data











