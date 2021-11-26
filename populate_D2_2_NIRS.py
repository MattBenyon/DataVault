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
    directory = 'Dataset2_Preautism_fNIRS-Data/fNIRS-Data/2daSessionDR'
    filepaths = []
    wl1Paths = []
    wl2Paths = []
    hdrPaths = []

    for i in range(1, 44):
        for filename in os.listdir(directory + "/Autism00" + str(i).zfill(2) + "-2" ):
            f = os.path.join(directory + "/Autism00" + str(i).zfill(2) + "-2", filename)
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

    conn = connect(
        dbname=db_name,
        user=db_user,
        host="localhost",
        password=db_password)

    cursor = conn.cursor()

    insert = "INSERT INTO SessionHUB (Source, timestamp) VALUES ('" + hashed_user + "', current_timestamp);"  # update description
    insertStatement(insert, conn, cursor)


def insertData(wl1Path, wl2Path, hdrPath, db_name, db_user, db_password, experimentalunitnumber, endpointnumber,
               treatmentnumber, DataSourceNumber):
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

        insert = "INSERT INTO DataSourceLINK (Source, timestamp, EndpointID, DataSourceID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
        cursor.execute(insert, (endpointnumber, DataSourceNumber))
        conn.commit()

        insert = "INSERT INTO Treatments (Source, timestamp, TreatmentID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, %s, %s);"
        cursor.execute(insert, (treatmentnumber, endpointnumber))
        conn.commit()

        insert = "INSERT INTO MeasuresLINK (Source, timestamp, SessionID, EndpointID) VALUES ('" + hashed_user + "', current_timestamp, 2, %s);"
        cursor.execute(insert, [endpointnumber])
        conn.commit()

        endpointnumber += 1

    cursor.close()

    return endpointnumber, treatmentnumber


def populateVault(db_name, db_user, db_password):
    print("\n*** POPULATING DATA VAULT WITH DATASET 2 - Session 2 ***")

    insertStaticData(db_name, db_user, db_password)

    wl1Paths, wl2Paths, hdrPaths, filepaths = getFilePaths()

    experimentalunitnumber = 11
    groupnumber = 0
    DataSourceNumber= 1
    endpointnumber = 511697
    treatmentnumber = 204

    filepath_length = len(wl1Paths)

    for i in range(filepath_length):
        print("\nUploading", i+1, "of", filepath_length, "...")
        endointnumber_temp, treatmentnumber = insertData(wl1Paths[i], wl2Paths[i], hdrPaths[i], db_name, db_user, db_password,
                                                         experimentalunitnumber,
                                                         endpointnumber, treatmentnumber, DataSourceNumber)

        endpointnumber = endointnumber_temp
        DataSourceNumber = 1
        treatmentnumber += 1
        experimentalunitnumber += 1