from .abstractModule import abstractModule
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import os
from .Utils.utils import load_graph, get_data
from .Graphs.Trace import Trace
from .Graphs.Trace import Bar
from .Graphs.Trace import Pie

class ArrangementResponsePieModule(abstractModule):

    sql_query_dropdown = "SELECT event_id, event_summary, timestamp_from " \
                         "FROM Dataplattform.EventRatingType " \
                         "WHERE event_button_name IS NOT NULL"

    db_connection = None

    style = {"width": "100%", "height": "100%", "display": "flex", "flexFlow": "column"}

    def __init__(self, app, connection=None):

        self.db_connection = connection

        df_dropdown = ((get_data(self.sql_query_dropdown)).drop_duplicates(subset=['event_id'])).reset_index()

        self.dccDropdown = dcc.Dropdown(
            id='event_dropdown',
            options=[
                {'label': df_dropdown['event_summary'][i],
                 'value': df_dropdown['event_id'][i]} for i in range(len(df_dropdown))
            ],
            value=df_dropdown['event_id'][0]
        )

        fig = Pie([0, 0, 0], ['Positive', 'Neutral', 'Negative'],
                  colors=['#55A868', '#ECEE70', '#BE4B27'])

        self.dccGraph = dcc.Graph(id='event_pie', figure=fig.get_trace(), style=self.graph_style)

    def get_module(self):
        return html.Div([
            self.dccDropdown,
            self.dccGraph
        ],
            style=self.style
        )

