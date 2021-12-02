
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
        #print(row)
        row = [float(x) for x in row]
        #print(row)
        rows.append(row)

    data = pd.DataFrame(rows)
    #print(data.head())
    data = data.dropna(axis='columns') # sometimes it adds in extra columns full of NaNs, this is a workaround



    return data




'''

def TimeSeries(data):

    fig = px.line(data)


    fig.update_layout(xaxis_title='Samples in time',
                     yaxis_title='Signal Strength',
                      legend_title_text='Channel')

    return fig
'''
experimentalunitID = 11
treatmentID = (experimentalunitID-10) + 160
SessionID = 1
datasourceID =1
data1 = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)

treatmentID = (experimentalunitID-10) + 203
SessionID = 2
data2 = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)
#subplot = TimeSeries(data1, data2)

def TimeSeries(data1, data2): 

    fig = make_subplots(rows = 2, cols = 1)
    
    fig.append_trace(go.Scatter(data1, mode='lines', name='channel'), row = 1, col = 1)
    
    fig.append_trace(go.Scatter(data2, mode='lines', name='channel'), row = 2, col = 1)
    
    fig.update_xaxes(title_text='Samples in time', row=1, col=1)
    fig.update_xaxes(title_text='Samples in time', row=2, col=1)
    
    fig.update_yaxes(title_text='Signal Strength', row=1, col=1)
    fig.update_yaxes(title_text='Signal Strength', row=2, col=1)
    '''
    fig1.update_layout(xaxis_title='Samples in time',
                     yaxis_title='Signal Strength',
                      legend_title_text='Channel')
    
    fig2 = px.line(data2)
    fig2.update_layout(xaxis_title='Samples in time',
                     yaxis_title='Signal Strength',
                      legend_title_text='Channel')
                      
    ***Make subplot from fig1 fig2***
    '''
    fig.show()



# below are the numbers to generate individual plots, above is how you would have subplots
'''
experimentalunitID = 11
treatmentID = (experimentalunitID-10) + 160
SessionID = 1
datasourceID =1
data = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)
fig1 = TimeSeries(data)
fig1.show()

experimentalunitID = 11
treatmentID = (experimentalunitID-10) + 203
SessionID = 2
datasourceID = 1
data = QueryUnit(experimentalunitID, treatmentID, SessionID, datasourceID)
fig2 = TimeSeries(data)
fig2.show()
'''
