# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from Tabs.slackTab import SlackTab

app_style={"width": "100vw", "height": "100vh"}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

slackTab = SlackTab()

app.layout = html.Div(children=slackTab.get_tab(), style=app_style)


if __name__ == '__main__':
	app.run_server(debug=True)
