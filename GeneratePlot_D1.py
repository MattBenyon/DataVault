
from psycopg2 import connect
import pandas as pd
import plotly.express as px
import numpy as np


def QueryData(experimentalunitID, datatypeID, treatmentID):
    conn = connect(
        dbname='v4_test',
        user='g09',
        host="localhost",
        password='g09')

    cursor = conn.cursor()
    select = ''' 
SELECT ObservedValue, EndpointHUB.EndpointID FROM EndpointHUB
INNER JOIN Treatments ON EndpointHUB.EndpointID = Treatments.EndpointID
INNER JOIN TreatmentHUB ON Treatments.TreatmentID = TreatmentHUB.TreatmentID
INNER JOIN EndpointUnitLink ON EndpointHUB.EndpointID = EndpointUnitLINK.EndpointID
INNER JOIN DataTypeLINK ON EndpointHUB.EndpointID = DataTypeLINK.EndpointID
WHERE EndpointUnitLINK.ExperimentalUnitID = %s AND DataTypeID = %s AND TreatmentHUB.TreatmentID = %s
ORDER BY EndpointHUB.EndpointID asc;

        '''

    cursor.execute(select, (experimentalunitID, datatypeID, treatmentID))
    result = cursor.fetchall()
    conn.close()

    rows = []
    for i in range(len(result)):
        row = result[i][0][1:-5]
        row = [float(x) for x in row]
        rows.append(row)





    data = pd.DataFrame(rows)
    #print(data)
    data = data.dropna(axis='columns') # sometimes it adds in extra columns full of NaNs, this is a workaround

    return data


def TimeSeries(data):

    variables_24 = {'0': 'CH1', '1': 'CH2','2': 'CH3','3': 'CH4','4': 'CH5',
                 '5': 'CH6', '6': 'CH7','7': 'CH8','8': 'CH9','9': 'CH10',
                 '10': 'CH11', '11': 'CH12', '12': 'CH13', '13': 'CH14', '14': 'CH15',
                 '15': 'CH16', '16': 'CH17', '17': 'CH18', '18': 'CH19', '19': 'CH20',
                 '20': 'CH21', '21': 'CH22', '22': 'CH23', '23': 'CH24'}

    variables_48 = {'0': 'CH1(WL1)', '1': 'CH1(WL2)', '2': 'CH2(WL1)', '3': 'CH2(WL2)', '4': 'CH3(WL1)',
                   '5': 'CH3(WL2)', '6': 'CH4(WL1)', '7': 'CH4(WL2)', '8': 'CH5(WL1)', '9': 'CH5(WL2)',
                   '10': 'CH6(WL1)', '11': 'CH6(WL2)', '12': 'CH7(WL1)', '13': 'CH7(WL2)', '14': 'CH8(WL1)',
                   '15': 'CH8(WL2)', '16': 'CH9(WL1)', '17': 'CH9(WL2)', '18': 'CH10(WL1)', '19': 'CH10(WL2)',
                   '20': 'CH11(WL1)', '21': 'CH11(WL2)', '22': 'CH12(WL1)', '23': 'CH12(WL2)',
                   '24': 'CH13(WL1)', '25': 'CH13(WL2)', '26': 'CH14(WL1)', '27': 'CH14(WL2)', '28': 'CH15(WL1)',
                   '29': 'CH15(WL2)', '30': 'CH16(WL1)', '31': 'CH16(WL2)', '32': 'CH17(WL1)', '33': 'CH17(WL2)',
                   '34': 'CH18(WL1)', '35': 'CH18(WL2)', '36': 'CH19(WL1)', '37': 'CH19(WL2)', '38': 'CH20(WL1)',
                   '39': 'CH20(WL2)', '40': 'CH21(WL1)', '41': 'CH21(WL2)', '42': 'CH22(WL1)', '43': 'CH22(WL2)',
                   '44': 'CH23(WL1)', '45': 'CH23(WL2)', '46': 'CH24(WL1)', '47': 'CH24(WL2)'
                   }

    fig = px.line(data)

    if len(data.columns) == 24:
        fig.for_each_trace(lambda t: t.update(name=variables_24[t.name],
                                          legendgroup=variables_24[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, variables_24[t.name])
                                          ))
    elif len(data.columns) == 48:
        fig.for_each_trace(lambda t: t.update(name=variables_48[t.name],
                                              legendgroup=variables_48[t.name],
                                              hovertemplate=t.hovertemplate.replace(t.name, variables_48[t.name])
                                              ))


    fig.update_layout(xaxis_title='Samples in time',
                     yaxis_title='Signal Strength',
                      legend_title_text='Channel')

    fig.show()

    return fig

def getInputs():

    experimentid = int(input("Enter the ExperimentID: "))

    experimentalunitID = int(input("Enter the ExperimentalUnitID: "))

    print("1: Moto, 2: Rest, 3: ViMo, 4: ViSo")
    treatmentChoice = int(input("Enter the treatment choice: "))

    print("1: deoxy, 2: oxy, 3: total, 4: MES")
    datatypeID = int(input("Enter the data type choice: "))

    treatmentid_s = np.arange(1,17)

    treatmentid_s = treatmentid_s + (16 * (experimentalunitID-1))
    #print(treatmentid_s)
    specific_treatment = ((treatmentChoice-1) * 4) + datatypeID
    #print(specific_treatment)
    TreatmentID = int(treatmentid_s[specific_treatment-1])
    print(experimentid, experimentalunitID, datatypeID, TreatmentID)
    return experimentid, experimentalunitID, datatypeID, TreatmentID

experimentid, experimentalunitID, datatypeID, TreatmentID = getInputs()
data = QueryData(experimentalunitID, datatypeID, TreatmentID)
TimeSeries(data)





