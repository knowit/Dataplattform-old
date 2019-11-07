from .abstractModule import abstractModule
import dash_core_components as dcc
import pandas as pd
from .Utils.utils import load_graph, get_data
from .Graphs.Trace import Trace
from datetime import datetime

class FagtimerTimeSeriesModule(abstractModule):
    sql_query = "SELECT reg_period, used_hours " \
                "FROM Dataplattform.UBWType " \
                "ORDER BY reg_period DESC"


    def __init__(self, app):
        df = get_data(self.sql_query)
        df = self.prepare_data(df)

        fig = Trace(
            df, data_layout=[["reg_period", "used_hours"]],
            title="Brukte fagtimer", axis_text=["tid", "timer"],
            axis_type=["date", "linear"], show_legend=False, line_fill=["tonexty", 0])

        self.dccGraph = dcc.Graph(figure=fig.get_trace(), style=self.graph_style)

    def get_module(self):
        return self.dccGraph

    def prepare_data(self, data):
        weeks = []
        for week in data['reg_period']:
            weeks.append(datetime.strptime(str(week)[:4] + "-W" + str(week)[4:] + "-5", "%Y-W%W-%w"))

        data['reg_period'] = weeks
        return data


