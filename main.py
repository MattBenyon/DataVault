# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:34:18 2021

@author: mattb
"""

import CreateDB
import Populate_D1
import time


def main():
    db_name, db_user, db_password = "vault_test","test","test"
    CreateDB.createDB(db_name, db_user,db_password)
    Populate_D1.PopulateVault(db_name, db_user, db_password)


    
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\nProgram executed in --- %s seconds ---" % round(time.time() - start_time))