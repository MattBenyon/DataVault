
from dash import Dash, dcc, html, Input, Output, callback_context

import numpy as np

import json

import GeneratePlot_D2_EEG

app = Dash(__name__)


app.layout = html.Div([

    html.H1("G09 Neuro Imaging Data Vault Dataset 2- Analytics Dash", style={'text-align': 'center'}),
    dcc.Dropdown(id="datasource",
                 options=[
                     {"label": "fNIRS", "value": 1},
                     {"label": "EEG", "value": 2},
                 ],
                 multi=False,
                 value= 2,
                 style={'width': "60%"}
                 ),
    dcc.Dropdown(id="experimentalunitID",
                 options=[
                     {"label": "Experimental Unit 1", "value": 1},
                     {"label": "Experimental Unit 2", "value": 2},
                     {"label": "Experimental Unit 3", "value": 3},
                     {"label": "Experimental Unit 4", "value": 4},
                     {"label": "Experimental Unit 5", "value": 5},
                     {"label": "Experimental Unit 6", "value": 6},
                     {"label": "Experimental Unit 7", "value": 7},
                     {"label": "Experimental Unit 8", "value": 8},
                     {"label": "Experimental Unit 9", "value": 9},
                     {"label": "Experimental Unit 10", "value": 10},
                    {"label": "Experimental Unit 1", "value": 1},
                     {"label": "Experimental Unit 2", "value": 2},
                     {"label": "Experimental Unit 3", "value": 3},
                     {"label": "Experimental Unit 4", "value": 4},
                     {"label": "Experimental Unit 5", "value": 5},
                     {"label": "Experimental Unit 6", "value": 6},
                     {"label": "Experimental Unit 7", "value": 7},
                     {"label": "Experimental Unit 8", "value": 8},
                     {"label": "Experimental Unit 9", "value": 9},
                     {"label": "Experimental Unit 10", "value": 10},
                    {"label": "Experimental Unit 1", "value": 1},
                     {"label": "Experimental Unit 2", "value": 2},
                     {"label": "Experimental Unit 3", "value": 3},
                     {"label": "Experimental Unit 4", "value": 4},
                     {"label": "Experimental Unit 5", "value": 5},
                     {"label": "Experimental Unit 6", "value": 6},
                     {"label": "Experimental Unit 7", "value": 7},
                     {"label": "Experimental Unit 8", "value": 8},
                     {"label": "Experimental Unit 9", "value": 9},
                     {"label": "Experimental Unit 10", "value": 10},
                    {"label": "Experimental Unit 1", "value": 1},
                     {"label": "Experimental Unit 2", "value": 2},
                     {"label": "Experimental Unit 3", "value": 3},
                     {"label": "Experimental Unit 4", "value": 4},
                     {"label": "Experimental Unit 5", "value": 5},
                     {"label": "Experimental Unit 6", "value": 6},
                     {"label": "Experimental Unit 7", "value": 7},
                     {"label": "Experimental Unit 8", "value": 8},
                     {"label": "Experimental Unit 9", "value": 9},
                     {"label": "Experimental Unit 10", "value": 10},
                    {"label": "Experimental Unit 1", "value": 1},
                     {"label": "Experimental Unit 2", "value": 2},
                     {"label": "Experimental Unit 3", "value": 3},
                 ],
                 multi=False,
                 value= 1,
                 style={'width': "60%"}
                 ),


    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='timeseries', figure={})

])



@app.callback(
    Output(component_id='timeseries', component_property='figure'),
    [Input(component_id='experimentalunitID', component_property='value'),
     Input(component_id='datasource', component_property='value')]
)

def update_graph(experimentalunitID, datasource):
    if datasource = 2:
        SessionID = 1
        experimentalunitID = experimentalunitID + 10
        data = GeneratePlot_D2_EEG.QueryUnit(experimentalunitID, SessionID, datasource)
        fig = GeneratePlot_D2_EEG.TimeSeries(data)
    elif datasource = 1:
        SessionID = 1
        experimentalunitID = experimentalunitID + 10
        data = GeneratePlot_D2_fNIRS.QueryUnit(experimentalunitID, SessionID, datasource)
        fig = GeneratePlot_D2_fNIRS.TimeSeries(data)

    return fig


import webbrowser
from threading import Timer


port = 5000

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))

if __name__ == '__main__':
    open_browser()
    app.run_server(port=port)



