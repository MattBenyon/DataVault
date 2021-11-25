import os
import readFiles_D2_NIRS
import hashlib
from psycopg2 import connect

def getData(wl1Path, wl2Path, hdrPath):
    expWl1Data = readFiles_D2_NIRS.getWl1Data(wl1Path)
    expWl2Data = readFiles_D2_NIRS.getWl2Data(wl2Path)
    MetaData = readFiles_D2_NIRS.getHDR(hdrPath)
    expData = readFiles_D2_NIRS.joinData(expWl1Data, expWl2Data)

    return expData, MetaData

def getFilePaths():
    directory = 'Dataset2_Preautism_fNIRS-Data\\fNIRS-Data\\1raSessionDR'
    filepaths = []
    wl1Paths = []
    wl2Paths = []
    hdrPaths = []

    for i in range(1, 44):
        for filename in os.listdir(directory + "\\Autism00" + str(i).zfill(2) + "-1" ):
            f = os.path.join(directory + "\\Autism00" + str(i).zfill(2) + "-1", filename)
            # checking if it is a file
            if os.path.isfile(f):
                filepaths.append(f)


    for path in filepaths:
        if ".wl1" in path:
            wl1Paths.append(path)
        if ".wl2" in path:
            wl2Paths.append(path)
        if ".hdr" in path:
            hdrPaths.append(path)

    return wl1Paths, wl2Paths, hdrPaths, filepaths


def insertStatement(insert, conn, cursor):
    cursor.execute(insert)
    conn.commit()

def insertStaticData(db_name, db_user, db_password):
    hashed_user = hashlib.md5(db_user.encode('utf-8')).hexdigest()
    experimentalunitnumber = 11

    conn = connect(
        dbname=db_name,
        user=db_user,
        host="localhost",
        password=db_password)

    cursor = conn.cursor()

    insert = "INSERT INTO researcherhub (Source, timestamp, Forename, Surname) VALUES ('" + hashed_user + "', current_timestamp, 'Zac', 'Webb');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO affiliation (ResearcherID, Source, timestamp, Affiliation) VALUES (2,'" + hashed_user + "', current_timestamp, 'University of Birmingham');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO experimenthub (Source, timestamp, Title) VALUES ('" + hashed_user + "', current_timestamp, 'A sample title test');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO experimentnosessions (ExperimentID, Source, timestamp, TypeByNoSession) VALUES (2,'" + hashed_user + "', current_timestamp, 'cross-sectional');"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO conducts (Source, timestamp, ExperimentID, ResearcherID) VALUES ('" + hashed_user + "', current_timestamp, 2, 2);"
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO DataType (Source, timestamp, Name) VALUES ('" + hashed_user + "', current_timestamp, 'fNIRS');"  # update description
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO SessionHUB (Source, timestamp) VALUES ('" + hashed_user + "', current_timestamp);"  # update description
    insertStatement(insert, conn, cursor)

    insert = "INSERT INTO ExperimentalUnitHUB (ExperimentalUnitID, Source, timestamp) VALUES (%s, '" + hashed_user + "', current_timestamp);"
    cursor.execute(insert, [experimentalunitnumber])
    conn.commit()


def insertData(wl1Path, wl2Path, hdrPath, db_name, db_user, db_password, experimentalunitnumber, endpointnumber,
               treatmentnumber, datatypenumber):
    expData, MetaData = getData(wl1Path, wl2Path, hdrPath)

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
        row = [str(x) for x in row]

        row = ",".join(row)
        row = "{"+row+"}"

        acquisition_time = "NULL"

        insert = "INSERT INTO EndpointHUB (Source, timestamp, ObservedValue, Acquistiontimestamp) VALUES (%s, current_timestamp, %s, %s);"  # update description
        cursor.execute(insert, (hashed_user, row, acquisition_time))
        conn.commit()


    MetaData = MetaData.replace("'", '"')
    insert = "INSERT INTO TreatmentHUB (Source, timestamp, Metadata) VALUES ('" + hashed_user + "', current_timestamp,'" + MetaData + "');"  # may want to add treatment description
    insertStatement(insert, conn, cursor)

    for i in range(row_count):


        insert = "INSERT INTO ObservesLINK (Source, timestamp, ExperimentID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, 2, %s);"
        cursor.execute(insert, [endpointnumber])
        conn.commit()

        insert = "INSERT INTO EndpointUnitLINK (Source, timestamp, ExperimentalUnitID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
        cursor.execute(insert, (experimentalunitnumber, endpointnumber))
        conn.commit()

        insert = "INSERT INTO DataTypeLINK (Source, timestamp, EndpointID, DataTypeID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
        cursor.execute(insert, (endpointnumber, datatypenumber))
        conn.commit()

        insert = "INSERT INTO Treatments (Source, timestamp, TreatmentID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
        cursor.execute(insert, (treatmentnumber, endpointnumber))
        conn.commit()


        insert = "INSERT INTO MeasuresLINK (Source, timestamp, SessionID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, 1, %s);"
        cursor.execute(insert, [endpointnumber])
        conn.commit()

        endpointnumber += 1

    cursor.close()

    return endpointnumber, treatmentnumber


def populateVault(db_name, db_user, db_password):
    print("\n*** POPULATING DATA VAULT WITH DATASET 2 - Session 1 ***")

    insertStaticData(db_name, db_user, db_password)

    wl1Paths, wl2Paths, hdrPaths, filepaths = getFilePaths()
    experimentalunitnumber = 11 # this has to start from 0 then be updated before calling function as 0 mod 16 is 0
    groupnumber = 0
    datatypenumber= 5
    endpointnumber = 443111
    treatmentnumber = 1

    filepath_length = len(wl1Paths) #CHANGE THIS WHEN NEEDED!
    #filepath_length = 1


    for i in range(filepath_length):
        print("\nUploading", i+1, "of", filepath_length, "...")
        #print(groupnumber, datatypenumber, treatmentnumber)
        endointnumber_temp, treatmentnumber = insertData(wl1Paths[i], wl2Paths[i], hdrPaths[i], db_name, db_user, db_password,
                                                         experimentalunitnumber,
                                                         endpointnumber, treatmentnumber, datatypenumber)

        endpointnumber = endointnumber_temp
        datatypenumber = 5
        treatmentnumber += 1