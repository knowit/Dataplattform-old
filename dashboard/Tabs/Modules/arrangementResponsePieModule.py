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

class ArrangementResponsePieModule(abstractModule):

    sql_query_dropdown = "SELECT event_id, event_summary, timestamp_from " \
                         "FROM Dataplattform.EventRatingType " \
                         "WHERE event_button_name IS NOT NULL"

    sql_query_pie = query = "SELECT positive_count, neutral_count, negative_count " \
                            "FROM Dataplattform.EventRatingType " \
                            "WHERE event_id = %s"

    db_connection = None
    callback_registered = False


    def __init__(self, app, connection=None):
        if not self.callback_registered:
            self.register_callbacks(app)
            self.callback_registered = True

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

        self.dccGraph = dcc.Graph(
            id='event_pie',
            figure={
                'data': [
                    {'labels': ['Positive', 'Neutral', 'Negative'],
                     'values': [0, 0, 0],
                     'type': 'pie'}
                ]
            },
            style=self.style
        )


    def get_module(self):
        return html.Div([
            self.dccDropdown,
            self.dccGraph
        ],
            style=self.style
        )


    def register_callbacks(self, app):
        @app.callback(Output('event_pie', 'figure'),
                      [Input('event_dropdown', 'value')])
        def chosen_event(value):
            df_pie = ((get_data(self.sql_query_pie, params=(value, ))).dropna()).sum()
            return {'data': [
                {
                    'labels': ['Positive', 'Neutral', 'Negative'],
                    'values': [df_pie['positive_count'], df_pie['neutral_count'], df_pie['negative_count']],
                    'type': 'pie'
                }]
            }
