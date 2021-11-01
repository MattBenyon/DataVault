# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 11:19:45 2021

@author: mattb
"""


import pandas as pd
import csv
import json



def getPatientInfo(filepath):

    patientInfo = []

    with open(filepath, encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf) 
            count = 0
            for row in csvReader:
                if count == 7: 
                    break
            
                elif count >=2: 
            
                    row['Attribute'] = row.pop('Header')
                    row['Values'] = row.pop(None)
                    patientInfo.append(row)
                    count = count + 1
                
                else:
                    count = count + 1
                    
    patientInfo_json = json.dumps(patientInfo, indent=2)
    return patientInfo_json
                
def getAnalyzeInfo(filepath):

    analyzeInfo = []

    with open(filepath, encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf) 
            count = 0
            for row in csvReader:
                if count == 16: 
                    break
            
                elif count >=8: 
            
                    row['Attribute'] = row.pop('Header')
                    row['Values'] = row.pop(None)
                    analyzeInfo.append(row)
                    count = count + 1
                
                else:
                    count = count + 1
                    
    analyzeInfo_json = json.dumps(analyzeInfo, indent=2)
    return analyzeInfo_json

def getMeasureInfo(filepath):

    measureInfo = []

    with open(filepath, encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf) 
            count = 0
            for row in csvReader:
                if count == 30:
                    break
               
                elif count == 26 or count == 27: 
                    count = count + 1
            
                elif count >=18: 
            
                    row['Attribute'] = row.pop('Header')
                    row['Values'] = row.pop(None)
                    measureInfo.append(row)
                    count = count + 1
                
                else:
                    count = count + 1
                
    measureInfo_json = json.dumps(measureInfo, indent=2)
    
    return measureInfo_json


def getStimTimes(filepath):

    stimTimes = []

    with open(filepath, encoding='utf-8') as csvf: 
            csvReader = csv.reader(csvf) 
            count = 0
            for row in csvReader:
            
                if count == 28: 
            
    
                    row = {row[i]: row[i + 1] for i in range(0, len(row), 2)}
                    stimTimes.append(row)
                   
                    break
                
                else:
                    count = count + 1
                    
    stimTimes_json = json.dumps(stimTimes, indent=2)
    return stimTimes_json
                
                
def getExpData(filepath):
    expData = pd.read_csv(filepath,
                   skiprows=40)
    
    return expData
    

patient = getPatientInfo('Dataset1_VM/VMData/VM0003_ViMo_HBA_Probe1_Total.csv')

            





    
        
