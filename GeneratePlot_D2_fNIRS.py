from psycopg2 import connect
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def getTreatment(treatmentID):
    conn = connect(
        dbname='g09_data_vault',
        user='g09',
        host="localhost",
        password='g09')

    cursor = conn.cursor()
    select = ''' 
            SELECT MetaData FROM TreatmentHUB WHERE TreatmentID = %s 
            '''

    cursor.execute(select, [treatmentID])
    result = cursor.fetchall()
    conn.close()

    return result


def QueryUnit(experimentalunitID, treatmentID, sessionID, datasourceID):
    conn = connect(
        dbname='g09_data_vault',
        user='g09',
        host="localhost",
        password='g09')

    print(experimentalunitID, treatmentID, sessionID)
    cursor = conn.cursor()
    select = ''' 
        SELECT EndpointHUB.EndpointID, ObservedValue FROM EndpointHUB
        INNER JOIN Treatments ON EndpointHUB.EndpointID = Treatments.EndpointID
        INNER JOIN TreatmentHUB ON Treatments.TreatmentID = TreatmentHUB.TreatmentID
        INNER JOIN EndpointUnitLink ON EndpointHUB.EndpointID = EndpointUnitLINK.EndpointID
        INNER JOIN MeasuresLINK ON MeasuresLINK.EndpointID = EndpointHUB.EndpointID
        INNER JOIN DataSourceLINK ON DataSourceLINK.EndpointID = EndpointHUB.EndpointID
        WHERE EndpointUnitLINK.ExperimentalUnitID = %s AND TreatmentHUB.TreatmentID = %s AND MeasuresLINK.SessionID = %s AND DataSourceLINK.DataSourceID = %s
        ORDER BY EndpointHUB.EndpointID asc;
        '''

    cursor.execute(select, (experimentalunitID, treatmentID, sessionID, datasourceID))
    result = cursor.fetchall()

    conn.close()

    rows = []
    for i in range(len(result)):
        row = result[i][1]
        # print(row)
        row = [float(x) for x in row]
        # print(row)
        rows.append(row)

    data = pd.DataFrame(rows)
    # print(data.head())
    data = data.dropna(axis='columns')  # sometimes it adds in extra columns full of NaNs, this is a workaround

    return data


'''

def TimeSeries(data):

    fig = px.line(data)


    fig.update_layout(xaxis_title='Samples in time',
                     yaxis_title='Signal Strength',
                      legend_title_text='Channel')

    return fig
'''


from psycopg2 import connect
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np


def getTreatment(treatmentID):
    conn = connect(
        dbname='g09_data_vault',
        user='g09',
        host="localhost",
        password='g09')

    cursor = conn.cursor()
    select = ''' 
            SELECT MetaData FROM TreatmentHUB WHERE TreatmentID = %s 
            '''

    cursor.execute(select, [treatmentID])
    result = cursor.fetchall()
    conn.close()

    return result


def QueryUnit(experimentalunitID, sessionID, datasourceID):
    conn = connect(
        dbname='g09_data_vault_test',
        user='g09',
        host="localhost",
        password='g09')


    cursor = conn.cursor()
    select = ''' 
        SELECT EndpointHUB.EndpointID, ObservedValue FROM EndpointHUB
        INNER JOIN EndpointUnitLink ON EndpointHUB.EndpointID = EndpointUnitLINK.EndpointID
        INNER JOIN MeasuresLINK ON MeasuresLINK.EndpointID = EndpointHUB.EndpointID
        INNER JOIN DataSourceLINK ON DataSourceLINK.EndpointID = EndpointHUB.EndpointID
        WHERE EndpointUnitLINK.ExperimentalUnitID = %s AND MeasuresLINK.SessionID = %s AND DataSourceLINK.DataSourceID = %s
        ORDER BY EndpointHUB.EndpointID asc;
        '''

    cursor.execute(select, (experimentalunitID, sessionID, datasourceID))
    result = cursor.fetchall()

    conn.close()

    rows = []
    for i in range(len(result)):
        row = result[i][1]
        # print(row)
        row = [float(x) for x in row]
        # print(row)
        rows.append(row)

    data = pd.DataFrame(rows)
    # print(data.head())
    data = data.dropna(axis='columns')  # sometimes it adds in extra columns full of NaNs, this is a workaround

    return data



def TimeSeries(data1, data2):
    fig = make_subplots(rows=2, cols=1)

    fig.append_trace(go.Scatter(data1, mode='lines', name='channel'), row=1, col=1)

    fig.append_trace(go.Scatter(data2, mode='lines', name='channel'), row=2, col=1)

    fig.update_xaxes(title_text='Samples in time', row=1, col=1)
    fig.update_xaxes(title_text='Samples in time', row=2, col=1)

    fig.update_yaxes(title_text='Signal Strength', row=1, col=1)
    fig.update_yaxes(title_text='Signal Strength', row=2, col=1)


    fig.show()


experimentalunitID = 11
SessionID = 1
datasourceID = 1
data1 = QueryUnit(experimentalunitID, SessionID, datasourceID)


SessionID = 2
data2 = QueryUnit(experimentalunitID, SessionID, datasourceID)


TimeSeries(data1, data2)
