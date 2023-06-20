import sqlite3

def create_connection(db_file: str):
    sql_connection = None

    try:
        sql_connection = sqlite3.connect(db_file)
        return sql_connection

    except sqlite3.Error as error:
        print(f"Greška kod kreiranja baze - {error}")
        return sql_connection
    
def create_table(sql_connection: sqlite3.Connection, create_table_sql: str):
    try:
        cursor = sql_connection.cursor()
        cursor.execute(create_table_sql)
        sql_connection.commit()
        cursor.close()
        return True
    
    except sqlite3.Error as error:
        print(f"Greška kod kreiranja tablice - {error}")
        return False
    
def insert_into_table(
    sql_connection: sqlite3.Connection, 
    insert_sql: str,
    data: list
):
    try:
        cursor = sql_connection.cursor()
        for item in data:
            cursor.execute(insert_sql, item)
        sql_connection.commit()
        cursor.close()
        return True
    
    except sqlite3.Error as error:
        print(f"Greška kod umetanja u tablicu - {error}")
        return False

def check_if_value_exists(
    sql_connection: sqlite3.Connection, 
    search_sql: str,
    data: list
):
    try:
        cursor = sql_connection.cursor()
        for item in data:
            cursor.execute(search_sql, item)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return True
        else:
            return False
    
    except sqlite3.Error as error:
        print(f"Greška kod pretrazivanja tablice - {error}")
        return False

def update_entry(sql_connection: sqlite3.Connection, 
    update_sql: str,
    data: list):
    try:
        cursor = sql_connection.cursor()
        cursor.execute(update_sql, data)
        sql_connection.commit()
        cursor.close()
    
    except sqlite3.Error as error:
        print(f"Greška kod promjene tablice - {error}")
        return False

def get_ID(
    sql_connection: sqlite3.Connection, 
    search_sql: str,
    data: list
):
    try:
        cursor = sql_connection.cursor()
        for items in data:
            cursor.execute(search_sql, items)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result
        else:
            return False
    
    except sqlite3.Error as error:
        print(f"Greška kod pretrazivanja tablice - {error}")
        return False

def get_data(
    sql_connection: sqlite3.Connection, 
    search_sql: str,
    data: list
):
    try:
        cursor = sql_connection.cursor()
        for item in data:
            cursor.execute(search_sql, item)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result
        else:
            return False
    
    except sqlite3.Error as error:
        print(f"Greška kod pretrazivanja tablice - {error}")
        return False

def delete_entry(sql_connection: sqlite3.Connection, 
    delete_sql: str,
):
    try:
        cursor = sql_connection.cursor()
        cursor.execute(delete_sql)
        print("Uspjesno smo izbrisali tablicu")
        cursor.close()
    
    except sqlite3.Error as error:
        print(f"Greška kod brisanja tablice - {error}")
        return False
#napraviti za brisanje podataka iz tablice

def db_len(sql_connection: sqlite3.Connection, 
    search_sql: str):

    try:
        cursor = sql_connection.cursor()
        cursor.execute(search_sql)
        result = cursor.fetchone()
        print("Uspjesno smo prebrojali tablicu")
        cursor.close()
        return result
    
    except sqlite3.Error as error:
        print(f"Greška kod brisanja tablice - {error}")
        return False
    

def get_all_data(
    sql_connection: sqlite3.Connection, 
    search_sql: str,
    data: list
):
    try:
        cursor = sql_connection.cursor()
        for item in data:
            cursor.execute(search_sql, item)
        result = cursor.fetchall()
        cursor.close()
        if result:
            return result
        else:
            return False
        
    except sqlite3.Error as error:
        print(f"Greška kod pretrazivanja tablice - {error}")
        return False