# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:34:18 2021

@author: mattb
"""

import CreateDB
import Populate_D1
import populate_D2_1_NIRS
import populate_D2_2_NIRS
import time
import populate_D2_EEG


def main():
    """Builds and populates the database."""
    
    db_user, db_password = "g09","g09"
    db_name = "g0_data_vault"

    CreateDB.createDB(db_name, db_user, db_password)
    Populate_D1.PopulateVault(db_name, db_user, db_password)
    populate_D2_1_NIRS.populateVault(db_name, db_user, db_password)
    populate_D2_2_NIRS.populateVault(db_name, db_user, db_password)
    populate_D2_EEG.populateVault(db_name,db_user, db_password)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\nProgram executed in --- %s seconds ---" % round(time.time() - start_time))
