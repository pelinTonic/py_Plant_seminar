from dbmanager.db_manager import *
import os

def Check_if_database_exists() -> bool:
    """_summary_

    Returns:
        bool: Provjerava postoji li baza podataka i tablica u bazi podataka
    """
    if os.path.exists("Pots.db"):

        conn = sqlite3.connect("Pots.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchone()
        
        if tables:
            return True
        else:
            return False
    else:
        False

def Select_from_pot() -> list:

    """_summary_

    Returns:
        List: Vraća listu sa svim vrijednostima u bazi podataka
    """

    conn = sqlite3.connect("Pots.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pot_data")
    result = cursor.fetchall()

    plants_from_db = []
    for row in result:
        plants_from_db.append(row)
    
    return plants_from_db

def Database_len():

    try:

        db_file = "Pots.db"

        search_sql = """
        SELECT COUNT(*) FROM pot_data
        """
        sql_connection = create_connection(db_file)
        result = db_len(sql_connection, search_sql)

        if result == False:
            result = 0
            return result
        else:
            return result
    
    except:

        result = 0
        return result