import pandas as pd
import json


def getWl1Data(filepath):
    expDataWl1 = pd.read_csv(filepath, delimiter=" ")

    return expDataWl1

def getWl2Data(filepath):
    expDataWl2 = pd.read_csv(filepath, delimiter=" ")

    return expDataWl2

def joinData(expDataWl1, expDataWl2):
    data = [expDataWl1, expDataWl2]
    expData = pd.concat(data, axis=1)

    return expData

def getHDR(filepath):
    HDR = {}

    with open(filepath) as data:

        for line in data:
            line = line.replace("\n", "")
            line = line.replace("\t", " ")
            try:
                if line[0] == "[":
                    sectionName = line[1:-1]
                    HDR[sectionName] = {}
                    currentSection = sectionName
                else:
                    tmpldx = line.find("=")
                    tmpKey = line[0:tmpldx]
                    tmpValue = line[tmpldx + 1:-1]

                    tmpDict = HDR[currentSection]
                    tmpDict[tmpKey] = tmpValue
                    HDR[currentSection] = tmpDict
            except IndexError:
                print()

    metaData = json.dumps(HDR)

    return(metaData)