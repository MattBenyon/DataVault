# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 13:36:07 2021

@author: mattb
"""
from psycopg2.extras import execute_values

import ReadFiles_D1

import os
from psycopg2 import connect
import hashlib
import json
import numpy as np


def getData(filepath):
    MetaData = json.dumps(ReadFiles_D1.getJSON(filepath))
    expData = ReadFiles_D1.getExpData(filepath)
        
    return expData, MetaData


def getFilePaths():
    
    directory = 'Dataset1_VM/VMData/'
    filepaths = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filepaths.append(f)
    return filepaths


def insertStatement(insert, conn, cursor):
    cursor.execute(insert)
    conn.commit()



def InsertStaticData(db_name, db_user,db_password):

    hashed_user = hashlib.md5(db_user.encode('utf-8')).hexdigest()

    conn = connect(
        dbname=db_name,
        user=db_user,
        host="localhost",
        password=db_password)

    cursor = conn.cursor()



    insert = "INSERT INTO researcherhub (Source, timestamp, Forename, Surname) VALUES ('"+hashed_user+"', current_timestamp, 'Matthew', 'Benyon');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO affiliation (ResearcherID, Source, timestamp, Affiliation) VALUES (1,'"+hashed_user+"', current_timestamp, 'University of Birmingham');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO experimenthub (Source, timestamp, Title) VALUES ('"+hashed_user+"', current_timestamp, 'A sample title');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO experimentnosessions (ExperimentID, Source, timestamp, TypeByNoSession) VALUES (1,'"+hashed_user+"', current_timestamp, 'longitudinal');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO conducts (Source, timestamp, ExperimentID, ResearcherID) VALUES ('"+hashed_user+"', current_timestamp, 1, 1);"
    insertStatement(insert, conn, cursor)


    #experimental unit insert with a for loop length of filepaths

    insert = "INSERT INTO DataSource (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'fNIRS');"  # update description
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'Oxy');"   # update description
    insertStatement(insert, conn, cursor)
    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'Deoxy');"  # update description
    insertStatement(insert, conn, cursor)
    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'Total');"  # update description
    insertStatement(insert, conn, cursor)
    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'MES');"  # update description
    insertStatement(insert, conn, cursor)


def InsertData(filepath, db_name, db_user, db_password,experimentalunitnumber, groupnumber, endpointnumber, treatmentnumber):

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

        row = expData.loc[i].to_list()
        row[1:]
        row = [str(x) for x in row]

        row = ",".join(row)

        insert = "INSERT INTO EndpointHUB (Source, timestamp, ObservedValue) VALUES (%s, current_timestamp, %s);"  # update description

        cursor.execute(insert, (hashed_user, row))
        conn.commit()


    for i in range(row_count):
        insert = "INSERT INTO ObservesLINK (Source, timestamp, ExperimentID, EndpointID) VALUES ('"+hashed_user+"', current_timestamp, 1 , %s);"
        cursor.execute(insert, [endpointnumber])
        conn.commit()
        endpointnumber += 1



    MetaData = MetaData.replace("'", '"')
    insert = "INSERT INTO TreatmentHUB (Source, timestamp, Metadata) VALUES ('"+hashed_user+"', current_timestamp,'" + MetaData + "');"  # may want to add treatment description
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO HasTreatmentsLINK (Source, timestamp, TreatmentID, ExperimentID) VALUES ('" + hashed_user + "', current_timestamp, %s,1);"
    cursor.execute(insert, [treatmentnumber])
    conn.commit()


    insert = "INSERT INTO GroupHUB (Source, timestamp, AllocationMethod) VALUES ('" + hashed_user + "', current_timestamp, 'within-subject');"
    insertStatement(insert, conn, cursor)


    insert = "INSERT INTO ExperimentalUnitHUB (Source, timestamp) VALUES ('" + hashed_user + "', current_timestamp);"
    insertStatement(insert, conn, cursor)


    insert = "INSERT INTO GroupsLINK(Source, timestamp, GroupID, ExperimentalUnitID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
    cursor.execute(insert, (groupnumber, experimentalunitnumber))
    conn.commit()

    cursor.close()

    return endpointnumber, treatmentnumber


def PopulateVault(db_name, db_user, db_password):
    print("\n*** POPULATING DATA VAULT WITH DATASET 1 ***")
    InsertStaticData(db_name, db_user, db_password)
    filepaths = getFilePaths()
    experimentalunitnumber = 1
    groupnumber = 1
    endpointnumber = 1
    treatmentnumber = 1
    for i in range(len(filepaths)):
        print("\nUploading", i, "of", len(filepaths),"...")
        endointnumber_temp, treatmentnumber = InsertData(filepaths[i], db_name, db_user, db_password,
                                                              experimentalunitnumber,
                                                              groupnumber, endpointnumber, treatmentnumber)

        endpointnumber = endointnumber_temp
        if (i % 4) == 0:
            experimentalunitnumber += 1
        groupnumber += 1
        if (i % 4) == 0:
            groupnumber = 1
        treatmentnumber += 1







