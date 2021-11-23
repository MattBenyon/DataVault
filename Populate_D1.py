# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 13:36:07 2021

@author: mattb
"""

import ReadFiles_D1

import os
from psycopg2 import connect
import hashlib
import json


def getData(filepath):
    MetaData = json.dumps(ReadFiles_D1.getJSON(filepath))
    expData = ReadFiles_D1.getExpData(filepath)

    return expData, MetaData


def getFilePaths():
    directory = 'Dataset1_VM/VMData/'
    filepaths = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            filepaths.append(f)
    return filepaths


def insertStatement(insert, conn, cursor):
    cursor.execute(insert)
    conn.commit()


def InsertStaticData(db_name, db_user, db_password):
    hashed_user = hashlib.md5(db_user.encode('utf-8')).hexdigest()

    conn = connect(
        dbname=db_name,
        user=db_user,
        host="localhost",
        password=db_password)

    cursor = conn.cursor()

    insert = "INSERT INTO researcherhub (Source, timestamp, Forename, Surname) VALUES ('" + hashed_user + "', current_timestamp, 'Matthew', 'Benyon');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO affiliation (ResearcherID, Source, timestamp, Affiliation) VALUES (1,'" + hashed_user + "', current_timestamp, 'University of Birmingham');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO experimenthub (Source, timestamp, Title) VALUES ('" + hashed_user + "', current_timestamp, 'A sample title');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO experimentnosessions (ExperimentID, Source, timestamp, TypeByNoSession) VALUES (1,'" + hashed_user + "', current_timestamp, 'longitudinal');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO conducts (Source, timestamp, ExperimentID, ResearcherID) VALUES ('" + hashed_user + "', current_timestamp, 1, 1);"
    insertStatement(insert, conn, cursor)

    # experimental unit insert with a for loop length of filepaths

    insert = "INSERT INTO DataSource (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'fNIRS');"  # update description
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'Oxy');"  # update description
    insertStatement(insert, conn, cursor)
    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'Deoxy');"  # update description
    insertStatement(insert, conn, cursor)
    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'Total');"  # update description
    insertStatement(insert, conn, cursor)
    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'MES');"  # update description
    insertStatement(insert, conn, cursor)

    for i in range(10):
        insert = "INSERT INTO ExperimentalUnitHUB (ExperimentalUnitID, Source, timestamp) VALUES (%s, '" + hashed_user + "', current_timestamp);"
        cursor.execute(insert, [i+1])
        conn.commit()


def InsertData(filepath, db_name, db_user, db_password, experimentalunitnumber, endpointnumber,
               treatmentnumber, datatypenumber):
    expData, MetaData = getData(filepath)

    hashed_user = hashlib.md5(db_user.encode('utf-8')).hexdigest()

    conn = connect(
        dbname=db_name,
        user=db_user,
        host="localhost",
        password=db_password)

    cursor = conn.cursor()

    row_count = len(expData.index)

    for i in range(row_count):

        acquisition_time = expData.loc[i].to_list()[-4]

        row = expData.loc[i].to_list()
        row[1:]
        row = [str(x) for x in row]

        row = ",".join(row)
        row = "{"+row+"}"

        insert = "INSERT INTO EndpointHUB (Source, timestamp, ObservedValue, Acquistiontimestamp) VALUES (%s, current_timestamp, %s, %s);"  # update description
        cursor.execute(insert, (hashed_user, row, acquisition_time))
        conn.commit()


    MetaData = MetaData.replace("'", '"')
    insert = "INSERT INTO TreatmentHUB (Source, timestamp, Metadata) VALUES ('" + hashed_user + "', current_timestamp,'" + MetaData + "');"  # may want to add treatment description
    insertStatement(insert, conn, cursor)


    for i in range(row_count):


        insert = "INSERT INTO ObservesLINK (Source, timestamp, ExperimentID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, 1 , %s);"
        cursor.execute(insert, [endpointnumber])
        conn.commit()

        insert = "INSERT INTO EndpointUnitLINK (Source, timestamp, ExperimentalUnitID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
        cursor.execute(insert, (experimentalunitnumber, endpointnumber))
        conn.commit()

        insert = "INSERT INTO DataSourceLINK (Source, timestamp, EndpointID, DataSourceID) VALUES ('" + hashed_user + "', current_timestamp, %s, 1);"
        cursor.execute(insert, [endpointnumber])
        conn.commit()

        insert = "INSERT INTO DataTypeLINK (Source, timestamp, EndpointID, DataTypeID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
        cursor.execute(insert, (endpointnumber, datatypenumber))
        conn.commit()

        insert = "INSERT INTO Treatments (Source, timestamp, TreatmentID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, %s,%s);"
        cursor.execute(insert, (treatmentnumber, endpointnumber))
        conn.commit()

        endpointnumber += 1


    cursor.close()

    return endpointnumber, treatmentnumber


def PopulateVault(db_name, db_user, db_password):
    print("\n*** POPULATING DATA VAULT WITH DATASET 1 ***")

    InsertStaticData(db_name, db_user, db_password)

    filepaths = getFilePaths()
    experimentalunitnumber = 0 # this has to start from 0 then be updated before calling function as 0 mod 16 is 0
    groupnumber = 0
    datatypenumber= 0
    endpointnumber = 1
    treatmentnumber = 1

    filepath_length = len(filepaths) #CHANGE THIS WHEN NEEDED!
    #filepath_length = 1


    for i in range(filepath_length):
        if (i % 16) == 0:
            experimentalunitnumber += 1
        if (i % 4) == 0:
            datatypenumber = 1
        print("\nUploading", i+1, "of", filepath_length, "...")
        #print(groupnumber, datatypenumber, treatmentnumber)
        endointnumber_temp, treatmentnumber = InsertData(filepaths[i], db_name, db_user, db_password,
                                                         experimentalunitnumber,
                                                         endpointnumber, treatmentnumber, datatypenumber)

        endpointnumber = endointnumber_temp
        datatypenumber += 1
        treatmentnumber += 1






