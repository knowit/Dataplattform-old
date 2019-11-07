from .abstractModule import abstractModule
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import os
from .Utils.utils import load_graph, get_data
from .Graphs.Trace import Trace
from .Graphs.Trace import Bar

class ArrangementResponseBarModule(abstractModule):
    sql_query = "SELECT event_summary, timestamp_from, positive_count, neutral_count, negative_count " \
                "FROM Dataplattform.EventRatingType " \
                "WHERE event_button_name IS NOT NULL " \
                "LIMIT 20"


    def __init__(self, app):

        df = (get_data(self.sql_query)).dropna()
        df = self.prepare_data(df)

        # positive_trace = {
        #     "name": "Positive",
        #     "type": "bar",
        #     "y": data['positive_count'],
        #     "x": xlabels,
        #     "text": data['event_summary'],
        #     "hovertemplate": 'Votes: %{y}'
        #                      '<br>%{text}',
        #     "marker": {
        #         "color": "#55A868"
        #     }
        # }
        # neutral_trace = {
        #     "name": "Neutral",
        #     "type": "bar",
        #     "y": data['neutral_count'],
        #     "x": xlabels,
        #     "text": data['event_summary'],
        #     "hovertemplate": 'Votes: %{y}'
        #                      '<br>%{text}',
        #     "marker": {
        #         "color": "#ECEE70"
        #     }
        # }
        #
        # negative_trace = {
        #     "name": "Negative",
        #     "type": "bar",
        #     "y": data['negative_count'],
        #     "x": xlabels,
        #     "text": data['event_summary'],
        #     "hovertemplate": 'Votes: %{y}'
        #                      '<br>%{text}',
        #     "marker": {
        #         "color": "#BE4B27"
        #     }
        # }

        # data = [positive_trace, neutral_trace, negative_trace]
        # layout = {
        #     "barmode": "stack",
        # }

        fig = Bar(
            df, data_layout=[["labels", "positive_count"], ["labels", "neutral_count"],
                             ["labels", "negative_count"]],
            title="Respons på siste arrangementer", axis_text=["Arrangement", "Stemmer"],
            names=["Positiv", "Nøytral", "Negative"], show_legend=True,
            show_yaxis_text=False, barmode="stack")

        self.dccGraph = dcc.Graph(figure=fig.get_trace(), style=self.graph_style)


    def get_module(self):
        return self.dccGraph


    def prepare_data(self, data):
        target_columns = ['positive_count', 'neutral_count', 'negative_count']

        # get all timestamps, remove duplicates and convert to datetime
        timestamps = (data[['event_summary', 'timestamp_from']]).drop_duplicates()
        timestamps['timestamp_from'] = pd.to_datetime(data['timestamp_from'], unit='s')

        # add votes from same events
        data = data.groupby(['event_summary'], as_index=False)[target_columns].sum()

        # merge with timestamps, sort by date and keep only the ten most recent events
        data = pd.merge(data, timestamps, on='event_summary', how='outer')
        data.sort_values(by=['timestamp_from'], inplace=True, ascending=True)
        data = data[-10:]

        # create custom x labels by slicing event summary and adding date
        truncated = data['event_summary'].str.slice(0, 25)
        truncated = truncated.apply(lambda x: x.ljust(28, '.') if len(x) >= 25 else x)
        formated_dates = data['timestamp_from'].dt.strftime("%d/%m-%y")
        xlabels = formated_dates.map(str) + ' ' + truncated.map(str)
        data['labels'] = xlabels

        return data




