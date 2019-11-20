from .abstractModule import abstractModule
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os
from .Utils.utils import load_graph, get_data
from .Graphs.Trace import Trace
from .Graphs.Trace import Bar
from datetime import datetime

class TwitterSearchHashtagDropdownModule(abstractModule):

    style = {"width": "100%", "height": "100%", "display": "flex", "flexFlow": "column"}

    def __init__(self):

        today = datetime.today().strftime("%Y-%m-%d")
        month_list_value = pd.date_range('2009-01-01', today,
                                   freq='MS')

        month_list_label = month_list_label.strftime("%Y-%b").tolist()
        month_list_label.append("Overall")
        month_list_value.append("Overall")
        month_list_label.reverse()
        month_list_value.reverse()

        self.dccDropdown = dcc.Dropdown(
            id='hashtag_dropdown',
            options=[
                {'label': month_list_label[i],
                 'value': month_list_value[i]} for i in range(len(month_list_label))
            ],
            value=month_list_value[1]
        )

        initial_df = pd.DataFrame()
        initial_df["freq"] = ""
        initial_df["hashtag"] = ""

        fig = Bar(
            initial_df, data_layout=[["freq", "hashtag"]],
            title="Mest brukte emneknagger", axis_text=["Antall", "Emneknagg"],
            names=["Emneknagg"], orientation="h", show_legend=False, show_yaxis_text=False)

        self.dccGraph = dcc.Graph(id='hashtag_month_bar', figure=fig.get_trace(), style=self.graph_style)



    def get_module(self):
        return html.Div([
            self.dccDropdown,
            self.dccGraph
        ],
            style=self.style
        )






