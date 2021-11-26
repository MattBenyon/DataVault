import mat73
import pandas as pd

def eegData(filepath):

    data_dict = mat73.loadmat(filepath)
    eegData = pd.DataFrame(data_dict['Data'])

    return eegData

def joinData(filepath1, filepath2):

    data_1 = mat73.loadmat(filepath1)
    data1 = pd.DataFrame(data_1['Data'])

    data_2 = mat73.loadmat(filepath2)
    data2 = pd.DataFrame(data_2['Data'])

    data = [data1, data2]

    joinedData = pd.concat(data, axis=1)

    return joinedData