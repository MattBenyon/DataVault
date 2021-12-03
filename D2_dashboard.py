
from dash import Dash, dcc, html, Input, Output, callback_context

import numpy as np

import json

import GeneratePlot_D2_EEG
import GeneratePlot_D2_fNIRS

app = Dash(__name__)


app.layout = html.Div(
    children= [
    html.Div([
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
                    {"label": "Experimental Unit 11", "value": 11},
                     {"label": "Experimental Unit 12", "value": 12},
                     {"label": "Experimental Unit 13", "value": 13},
                     {"label": "Experimental Unit 14", "value": 14},
                     {"label": "Experimental Unit 15", "value": 15},
                     {"label": "Experimental Unit 16", "value": 16},
                     {"label": "Experimental Unit 17", "value": 17},
                     {"label": "Experimental Unit 18", "value": 18},
                     {"label": "Experimental Unit 19", "value": 19},
                     {"label": "Experimental Unit 20", "value": 20},
                    {"label": "Experimental Unit 21", "value": 21},
                     {"label": "Experimental Unit 22", "value": 22},
                     {"label": "Experimental Unit 23", "value": 23},
                     {"label": "Experimental Unit 24", "value": 24},
                     {"label": "Experimental Unit 25", "value": 25},
                     {"label": "Experimental Unit 26", "value": 26},
                     {"label": "Experimental Unit 27", "value": 27},
                     {"label": "Experimental Unit 28", "value": 28},
                     {"label": "Experimental Unit 29", "value": 29},
                     {"label": "Experimental Unit 30", "value": 30},
                    {"label": "Experimental Unit 31", "value": 31},
                     {"label": "Experimental Unit 32", "value": 32},
                     {"label": "Experimental Unit 33", "value": 33},
                     {"label": "Experimental Unit 34", "value": 34},
                     {"label": "Experimental Unit 35", "value": 35},
                     {"label": "Experimental Unit 36", "value": 36},
                     {"label": "Experimental Unit 37", "value": 37},
                     {"label": "Experimental Unit 38", "value": 38},
                     {"label": "Experimental Unit 39", "value": 39},
                     {"label": "Experimental Unit 40", "value": 40},
                    {"label": "Experimental Unit 41", "value": 41},
                     {"label": "Experimental Unit 42", "value": 42},
                     {"label": "Experimental Unit 43", "value": 43},
                 ],
                 multi=False,
                 value= 1,
                 style={'width': "60%"}
                 ),


    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='timeseries1', figure={}),
    ]),#
    html.Div([
    dcc.Graph(id='timeseries2', figure={})])
    ])






@app.callback(
    [Output(component_id='timeseries1', component_property='figure'),
    Output(component_id='timeseries2', component_property='figure')],
    [Input(component_id='experimentalunitID', component_property='value'),
     Input(component_id='datasource', component_property='value')]
)

def update_graph(experimentalunitID, datasource):
    if datasource == 2:
        SessionID = 1
        experimentalunitID = experimentalunitID + 10
        data = GeneratePlot_D2_EEG.QueryUnit(experimentalunitID, SessionID, datasource)
        fig1 = GeneratePlot_D2_EEG.TimeSeries(data)
        SessionID = 2
        data = GeneratePlot_D2_EEG.QueryUnit(experimentalunitID, SessionID, datasource)
        fig2 = GeneratePlot_D2_EEG.TimeSeries(data)
    elif datasource == 1:
        SessionID = 1
        experimentalunitID = experimentalunitID + 10
        data = GeneratePlot_D2_fNIRS.QueryUnit(experimentalunitID, SessionID, datasource)
        fig1 = GeneratePlot_D2_fNIRS.TimeSeries(data)
        SessionID = 2
        data = GeneratePlot_D2_fNIRS.QueryUnit(experimentalunitID, SessionID, datasource)
        fig2 = GeneratePlot_D2_fNIRS.TimeSeries(data)

    return fig1, fig2


import webbrowser

port = 5000

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))

if __name__ == '__main__':
    open_browser()
    app.run_server(port=port)



