# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:06:25 2021

@author: mattb
"""

from psycopg2 import connect


def createDB(db_name, db_user,db_password):
    """Reads commands from DataVaultV4.txt to build the data vault."""
    
    try:

        conn = connect(
            dbname=db_name,
          user=db_user,
          host="localhost",
          password=db_password)

        cursor = conn.cursor()

        with open("DataVaultV4.txt") as f:
          vault_script = f.read()

        print("Creating database...")
        cursor.execute(vault_script)

        conn.commit()

        cursor.close()

        conn.close()

    except:
        print("\nThe credentials were incorrect or the user does not have correct permissions. Please correct this issue and run the program again.")
        quit()
