
from dash import Dash, dcc, html, Input, Output, callback_context

import numpy as np

import json

import GeneratePlot_D1

app = Dash(__name__)


app.layout = html.Div([

    html.H1("G09 Neuro Imaging Data Vault - Analytics Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="experimentalunitID",
                 options=[
                     {"label": "Average", "value": 11},
                     {"label": "Experimental Unit 1", "value": 1},
                     {"label": "Experimental Unit 2", "value": 2},
                     {"label": "Experimental Unit 3", "value": 3},
                     {"label": "Experimental Unit 4", "value": 4},
                     {"label": "Experimental Unit 5", "value": 5},
                     {"label": "Experimental Unit 6", "value": 6},
                     {"label": "Experimental Unit 7", "value": 7},
                     {"label": "Experimental Unit 8", "value": 8},
                     {"label": "Experimental Unit 9", "value": 9},
                     {"label": "Experimental Unit 10", "value": 10}
                 ],
                 multi=False,
                 value= 11,
                 style={'width': "60%"}
                 ),

    dcc.Dropdown(id="datatypeID",
                 options=[
                     {"label": "Deoxy", "value": 1},
                     {"label": "Oxy", "value": 2},
                     {"label": "Total", "value": 3},
                     {"label": "MES", "value": 4},
                 ],
                 multi=False,
                 value= 1,
                 style={'width': "60%"}
                 ),

    dcc.Dropdown(id="treatmentChoice",
                 options=[
                     {"label": "Moto", "value": 1},
                     {"label": "Rest", "value": 2},
                     {"label": "ViMo", "value": 3},
                     {"label": "ViSo", "value": 4},
                 ],
                 multi=False,
                 value= 1,
                 style={'width': "60%"}
                 ),

    html.Button("Download Metadata JSON file", id="btn-download", style={'width': "36%"}, n_clicks = 0),
    dcc.Download(id="download"),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='timeseries', figure={})

])



@app.callback(
    Output(component_id='timeseries', component_property='figure'),
    [Input(component_id='experimentalunitID', component_property='value'),
     Input(component_id='datatypeID', component_property='value'),
     Input(component_id='treatmentChoice', component_property='value')]
)
def update_graph(experimentalunitID, datatypeID, treatmentChoice):


    treatmentid_s = np.arange(1, 17)
    experimentalunitID = int(experimentalunitID)

    if experimentalunitID == 11:
        experimentalunitID = np.arange(0, 10)
        treatmentid_s = (16 * (experimentalunitID)) + 1
        specific_treatment = ((treatmentChoice - 1) * 4) + datatypeID
        treatmentid_s = treatmentid_s + (specific_treatment - 1)
        TreatmentID = treatmentid_s

        df = GeneratePlot_D1.QueryAllUnits(datatypeID, TreatmentID)
        fig = GeneratePlot_D1.TimeSeriesAverage(df)

    else:
        treatmentid_s = treatmentid_s + (16 * (experimentalunitID - 1))
        specific_treatment = ((treatmentChoice - 1) * 4) + datatypeID
        TreatmentID = int(treatmentid_s[specific_treatment - 1])

        df = GeneratePlot_D1.QueryUnit(experimentalunitID, datatypeID, TreatmentID)
        fig = GeneratePlot_D1.TimeSeries(df)

    return fig



@app.callback(
    Output("download", "data"),
    [Input("btn-download", "n_clicks"), Input(component_id='experimentalunitID', component_property='value'),
     Input(component_id='datatypeID', component_property='value'),
     Input(component_id='treatmentChoice', component_property='value')],
    prevent_initial_call=True,)

def func(n_clicks, experimentalunitID, datatypeID, treatmentChoice):

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if 'btn-download' in changed_id:
        if experimentalunitID == 11:
            nothing = dict(content="There is no metadata for the average", filename="average.txt")
            return nothing

        else:
            DT =["Deoxy","Oxy","Total","MES"]
            T = ["Moto", "Rest", "ViMo", "ViSo"]

            treatmentid_s = np.arange(1, 17)
            treatmentid_s = treatmentid_s + (16 * (experimentalunitID - 1))
            specific_treatment = ((treatmentChoice - 1) * 4) + datatypeID
            TreatmentID = int(treatmentid_s[specific_treatment - 1])


            filename = "VM" + str(experimentalunitID) + "_" + DT[datatypeID] + "_" + T[treatmentChoice] + ".json"
            content = GeneratePlot_D1.getTreatment(TreatmentID)
            content = json.dumps(content[0], indent = 4)
            return dict(content=content, filename=filename)



import webbrowser
from threading import Timer


port = 5000

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))

if __name__ == '__main__':
    open_browser()
    app.run_server(port=port)



