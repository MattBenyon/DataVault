
from dash import Dash, dcc, html, Input, Output

import numpy as np

import GeneratePlot_D1

app = Dash(__name__)


# App layout
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
                 value=11,
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
                 value=1,
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
                 value=1,
                 style={'width': "60%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='timeseries', figure={})

])



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='timeseries', component_property='figure')],
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
        container = ""

    else:
        treatmentid_s = treatmentid_s + (16 * (experimentalunitID - 1))
        specific_treatment = ((treatmentChoice - 1) * 4) + datatypeID
        TreatmentID = int(treatmentid_s[specific_treatment - 1])
        container = ""

        df = GeneratePlot_D1.QueryUnit(experimentalunitID, datatypeID, TreatmentID)
        fig = GeneratePlot_D1.TimeSeries(df)

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
