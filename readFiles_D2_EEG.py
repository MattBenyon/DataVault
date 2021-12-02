import mat73
import numpy as np


def eegData(filepath):

    data_dict = mat73.loadmat(filepath)
    eegData = data_dict['Data']

    return eegData

def joinData(filepath1, filepath2):

    data_1 = mat73.loadmat(filepath1)
    data1 = data_1['Data']

    data_2 = mat73.loadmat(filepath2)
    data2 = data_2['Data']

    data = [data1, data2]

    joinedData = np.concatenate(data, axis=1)

    return joinedData
