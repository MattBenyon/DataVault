from psycopg2 import connect
import pandas as pd
import plotly.express as px
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

    print(experimentalunitID, treatmentID, sessionID, datasourceID)
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


def TimeSeries(data):
    fig = px.line(data)

    fig.update_layout(xaxis_title='Samples in time',
                      yaxis_title='Signal Strength',
                      legend_title_text='Channel')

    return fig


'''
def TimeSeries(data1, data2):
    fig1 = px.line(data)
    fig1.update_layout(xaxis_title='Samples in time',
                     yaxis_title='Signal Strength',
                      legend_title_text='Channel')

    fig2 = px.line(data)
    fig2.update_layout(xaxis_title='Samples in time',
                     yaxis_title='Signal Strength',
                      legend_title_text='Channel')

    ***Make subplot from fig1 fig2***

    return the subplot

experimentalunitID = 11
treatmentID = (experimentalunitID-10) + 160
SessionID = 1
datasourceID =1
data1 = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)
treatmentID = (experimentalunitID-10) + 203
SessionID = 2
data2 = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)
subplot = TimeSeries(data1, data2)

'''

# below are the numbers to generate individual plots, above is how you would have subplots

experimentalunitID = 11
treatmentID = (experimentalunitID - 10) + 160
SessionID = 1
datasourceID = 2
data = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)
fig1 = TimeSeries(data)
fig1.show()

experimentalunitID = 11
treatmentID = (experimentalunitID - 10) + 203
SessionID = 2
data = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)
fig2 = TimeSeries(data)
fig2.show()
