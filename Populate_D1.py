# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 13:36:07 2021

@author: mattb
"""

import ReadFiles_D1

import os



def getData(filepath):
    patientInfo = ReadFiles_D1.getPatientInfo(filepath)
    analyzeInfo = ReadFiles_D1.getAnalyzeInfo(filepath)
    measureInfo = ReadFiles_D1.getMeasureInfo(filepath)
    stimTimes = ReadFiles_D1.getStimTimes(filepath)
    expData = ReadFiles_D1.getExpData(filepath)
        
    return patientInfo, analyzeInfo, measureInfo, stimTimes, expData


def getFilePaths():
    
    directory = 'Dataset1_VM/VMData/'
    filepaths = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filepaths.append(f)
    return filepaths


patientInfo, analyzeInfo, measureInfo, stimTimes, expData = getData('Dataset1_VM/VMData/VM0001_Moto_HBA_Probe1_Deoxy.csv')

print(patientInfo, analyzeInfo, measureInfo, stimTimes, expData)

        




