# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from get_data import get_data, get_all_events

ind = ['ad', 'sdsds']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#4B6455',
    'text': '#F1F0ED'
}

#DETTE MÅ RYDDES OPP
event_data, summarized_event_data = get_data("gfdg")

all_events = get_all_events()

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Knowit Pulsen',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.H2("Eventbox Feedback",
            style={'color': colors['text']}),

    html.Div(
        [
            dcc.Dropdown(
                id='event-dropdown',
                options=[{'label': name['event_summary'],
                          'value': event_data.index(name)} for name in event_data]
            )
        ],
        style={'width': '50%',
               'display': 'inline-block'}),

    dcc.Graph(
        id='pie-yo',
        figure={
            'data': [
                {'labels': ['Positive', 'Neutral', 'Negative'], 'values': [2, 1, 5], 'type': 'pie'}
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),


    html.Div(children='Eventbox Feedback', style={
        'textAlign': 'center',
        'color': colors['text']
    }),


    dcc.Graph(
        id='pie-all',
        figure={
            'data': [
                {'labels': ['Positive', 'Neutral', 'Negative'],
                 'values':[summarized_event_data['positive_count'], summarized_event_data['neutral_count'], summarized_event_data['negative_count']],
                 'type': 'pie'}
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
])



@app.callback(
    dash.dependencies.Output('pie-yo', 'figure'),
    [dash.dependencies.Input('event-dropdown', 'value')])
def set_display_children(selected_value):
    if not selected_value:
        values = [event_data[0]['positive_count'],
                  event_data[0]['neutral_count'],
                  event_data[0]['negative_count']]
    else:
        values = [event_data[selected_value]['positive_count'],
                  event_data[selected_value]['neutral_count'],
                  event_data[selected_value]['negative_count']]


    return {'data': [{'labels': ['Positive', 'Neutral', 'Negative'], 'values': values, 'type': 'pie'}],
            'layout': {'plot_bgcolor': colors['background'], 'paper_bgcolor': colors['background'], 'font': {'color': colors['text']}}}


if __name__ == '__main__':
    app.run_server(debug=True)



