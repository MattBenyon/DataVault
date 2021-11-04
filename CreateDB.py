from psycopg2 import connect


def createDB(db_name, db_user,db_password):
    print("Creating database...")
    conn = connect(
        dbname=db_name,
        user=db_user,
        host="localhost",
        password=db_password)

    cursor = conn.cursor()

    with open("DataVaultV3.txt") as f:
        vault_script = f.read()


    cursor.execute(vault_script)

    conn.commit()

    cursor.close()

    conn.close()
