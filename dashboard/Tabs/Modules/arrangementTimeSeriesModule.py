from .abstractModule import abstractModule
import dash_core_components as dcc
import pandas as pd
from .Utils.utils import load_graph, get_data
from .Graphs.Trace import Trace


class ArrangementTimeSeriesModule(abstractModule):
    sql_query = "SELECT timestamp_from, event_summary, calendar_id " \
                "FROM Dataplattform.EventRatingType" \


    def __init__(self, app):
        df = (get_data(self.sql_query)).drop_duplicates()
        df = self.prepare_data(df)

        fig = Trace(
            df, data_layout=[["timestamp_from", "all"], ["timestamp_from", "event_kalender"],
                             ["timestamp_from", "fag_kalender"]],
            title="Arrangementer pr måned", axis_text=["Dato", "Arrangementer"],
            names=["Alle", "Knowit Events", "Knowit Fagkalender"],
            axis_type=["date", "linear"], show_legend=True, line_fill=["tonexty", 0])

        self.dccGraph = dcc.Graph(figure=fig.get_trace(), style=self.graph_style)

    def get_module(self):
        return self.dccGraph

    def prepare_data(self, data):
        calendar_id = {
            "fag_kalender": "knowit.no_63rtu1seerufqsdhc4avduoggk@group.calendar.google.com",
            "event_kalender": "knowit.no_rsgaebrj8ihghga8scoqu5i6c0@group.calendar.google.com"
        }

        data['timestamp_from'] = pd.to_datetime(data['timestamp_from'], unit='s')
        data = data.set_index(data['timestamp_from'])

        for calendar in calendar_id:
            data[calendar] = 0
            data.loc[data.calendar_id == calendar_id[calendar], calendar] = 1

        data['all'] = 1
        data = data.resample('M').sum()
        data['timestamp_from'] = data.index
        return data


