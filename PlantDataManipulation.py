from dbmanager.db_manager import *

def Change_plant_data(name_entry: str, minHum_entry: str, maxHum_entry: str, minTemp_entry: str, maxTemp_entry:str, ph_entry: str, light_entry: str, id:str):

    """
    Odjavljuje korisnika iz aplikacije
    Args:
        name_entry(str): Ime biljke
        minHum_entry(str): minimalna vlažnost
        maxHum_entry(str):  maksimalna vlažnost
        minTemp_entry(str): minimalna temperatura
        maxTemp_entry(str): maksimalna temperatura
        ph_entry(str):  ph
        light_entry(str): svijetlost
        id(str): id biljke u bazi podataka
    """

    db_file = "Plants.db"

    minHum_entry = minHum_entry.replace("%","")
    maxHum_entry = maxHum_entry.replace("%","")
    minTemp_entry = minTemp_entry.replace("°C","")
    maxTemp_entry = maxTemp_entry.replace("°C","")
    
    sql_connection = create_connection(db_file)
    update_sql = """UPDATE Plants SET Name = ?, minSoilHumidity = ?, maxSoilHumidity = ?, minTemperature = ?, maxTemperature = ?,pH =?, Light = ? WHERE Id = ?"""
    data = (name_entry, minHum_entry, maxHum_entry, minTemp_entry, maxTemp_entry,ph_entry, light_entry, id)

    update_entry(sql_connection, update_sql, data)

def Database_len():
    db_file = "Plants.db"

    search_sql = """
    SELECT COUNT(*) FROM Plants
    """
    sql_connection = create_connection(db_file)
    result = db_len(sql_connection, search_sql)


    return result
    
def Select_Data_From_Database():

    conn = sqlite3.connect("Plants.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Plants")
    result = cursor.fetchall()

    plants_from_db = []
    for row in result:
        plants_from_db.append(row)
    
    return plants_from_db
    
def ID_plant(name: str):
    """
    Dohvaća ID biljke
    """

    db_file = "Plants.db"

    search_sql = """
        SELECT id from Plants WHERE Name = ?
        """
    sql_connection =create_connection(db_file)
    data = [(name,)]


    search = get_ID(sql_connection, search_sql, data)
    search = search[0]

    return search  

def Get_plant_data(name: str):
    """Dohvaća podatke iz baze podataka
    Args: 
        name(str) : ime biljke za koju se traže podatci
    """
    db_file = "Plants.db"

    search_sql = """
        SELECT * from Plants WHERE Name = ?
        """
    sql_connection =create_connection(db_file)
    data = [(name,)]


    search = get_all_data(sql_connection, search_sql, data)
    search = search[0]

    return search  
