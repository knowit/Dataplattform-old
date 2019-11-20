import dash_html_components as html
#import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import pandas as pd

from Tabs.slackTab import SlackTab
from Tabs.twitterTab import TwitterTab
from Tabs.arrangementTab import ArrangementTab
from Tabs.fagtimerTab import FagtimerTab
from Tabs.Modules.Utils.utils import load_graph, get_data


#slackTab = SlackTab()
#twitterTab = TwitterTab()


colors = {
    'background': '#4B6455',
    'text': '#333333'
}


tabs_colors = {
    'border': "#B7DEBD",
    'primary': "black",
    'background': "#B7DEBD",
}


tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'color': '#333333',
    'font-family': 'Arial',
    'font-size': '100%',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#f2f9ff',
    'color': '#333333',
    'font-family': 'Arial',
    'font-size': '100%',
    'fontWeight': 'bold'
}

def get_layout(app):
    tabs = dcc.Tabs(
        children=[
            dcc.Tab(label="FAGTIMER",
                    id="fagTab",
                    value="fag_value",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    ),

            dcc.Tab(label="SLACK",
                    id="slackTab",
                    value="slack_value",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    ),

            dcc.Tab(label="ARRANGEMENT",
                    id="arrTab",
                    value="arr_value",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    ),

            dcc.Tab(label="TWITTER",
                    id="twiTab",
                    value="twi_value",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    ),

        ],
        id="tabs",
        value='fag_value',
        colors=tabs_colors
    )

    content = html.Div(id='content',
                       style={
                           'height': '100%',
                           'width': '100%'
                       })

    layout = html.Div(
        children=[
            tabs,
            content
        ],
        style={'width': '100vw',
               'height': '100vh'}
    )
    return layout



def register_callbacks(app):
    @app.callback(Output('content', 'children'),
                  [Input('tabs', 'value')])
    def render_content(tab):
        if tab == "fag_value":
            return FagtimerTab(app).get_tab()
        elif tab == "slack_value":
            return SlackTab(app).get_tab()
        elif tab == "arr_value":
            return ArrangementTab(app).get_tab()
        elif tab == "twi_value":
            return TwitterTab(app).get_tab()

    # traverse all components and register callbacks
    @app.callback(Output('event_pie', 'figure'),
                  [Input('event_dropdown', 'value')],
                  [State('event_pie', 'figure')])
    def chosen_event(value, fig):
        sql_query_pie = "SELECT positive_count, neutral_count, negative_count " \
                                "FROM Dataplattform.EventRatingType " \
                                "WHERE event_id = %s"

        df_pie = ((get_data(sql_query_pie, params=(value, ))).dropna()).sum()
        fig['data'] = [
            {
                'labels': ['Positive', 'Neutral', 'Negative'],
                'values': [df_pie['positive_count'], df_pie['neutral_count'], df_pie['negative_count']],
                'type': 'pie',
                'marker': {'colors': ['#55A868', '#ECEE70', '#BE4B27']
                }
            }]

        return fig

    @app.callback(Output('hashtag_month_bar', 'figure'),
                  [Input('hashtag_dropdown', 'value')],
                  [State('hashtag_month_bar', 'figure')])
    def chosen_hashtag_month(value, fig):


        sql_query = "SELECT created, hashtags " \
                    "FROM Dataplattform.TwitterSearchType " \
                    "WHERE hashtags <> '' " \
                    "AND (created BETWEEN '2019-04-01' AND '2019-05-01') " \

        data = get_data(sql_query)

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
        freq = freq[-10:]

        fig['data'] = [
            {
                'y': freq['hashtag'],
                'x': freq['freq'],
                'type': 'bar',
                'orientation': 'h',

            }]

        return fig
