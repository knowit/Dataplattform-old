# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from layout import get_layout
from layout import register_callbacks

from Tabs.slackTab import SlackTab
from Tabs.twitterTab import TwitterTab

app_style={"width": "100vw", "height": "100vh"}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

app.layout = get_layout(app)
register_callbacks(app)

# slackTab = SlackTab()
# twitterTab = TwitterTab()
#
#
# app.layout = html.Div(children=twitterTab.get_tab(), style=app_style)


if __name__ == '__main__':
	app.run_server(debug=True)
