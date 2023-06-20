import sqlite3
import random
from temperatura_API import *

class Biljke:
    def __init__(self, database) -> None:

        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Plants (
            id INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            minSoilHumidity INTEGER NOT NULL,
            maxSoilHumidity INTEGER NOT NULL,
            minTemperature INTEGER NOT NULL,
            maxTemperature INTEGER NOT NULL,
            pH INTEGER NOT NULL,
            Light TEXT NOT NULL,
            Photo TEXT NOT NULL );

            """ 
        )  
        self.conn.commit()

    def fetch(self):
        self.cursor.execute("SELECT * FROM Plants")
        rows = self.cursor.fetchall()
        return rows
    
    def insert(self, Name, minSoilHumidity, maxSoilHumidity, minTemperature, maxTemperature,ph, Light, Photo):
        self.cursor.execute("INSERT INTO Plants (Name, minSoilHumidity, maxSoilHumidity, minTemperature, maxTemperature, pH, Light, Photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (Name, minSoilHumidity, maxSoilHumidity, minTemperature, maxTemperature, ph, Light, Photo,))
        self.conn.commit()


    def remove(self, id):
        self.cursor.execute("DELETE FROM Plants WHERE id=?", (id,))
        counter = 0
        counter += 1
        self.conn.commit()
        return counter

    def __del__(self):
        self.conn.close()
        
class Senzor:
    
    def Temperatura():
        temp = get_current_temperature()
    
        temp = temp.strip("+°C")
        temp = int(temp)
        temperature = random.randint(temp-1, temp+1)
        return temperature
    
    def Soil_humidity():
        soil_humidity = random.randint(10,90)
        return soil_humidity

    def pH():
        ph = random.uniform(5.55,8.75)
        ph = round(ph, 2)
        return ph
    def light():
        light = random.randint(40, 100)
        return light
    def upadate():
        temperatura = Senzor.Temperatura()
        ph = Senzor.pH()
        soil = Senzor.Soil_humidity()
        light = Senzor.light()

        return temperatura, ph, soil, light
    
    def get_senzor_data():

        data = Senzor.upadate()

        counter = 0
        temperature_data = []
        ph_data = []
        soil_data = []
        light_data = []

        while counter < 12:

            temperature = int(data[0]) + random.randint(-5,5)
            temperature_data.append(temperature)

            ph_change = random.uniform(-0.5,0.8)
            ph_change = round(ph_change, 2)
            ph = int(data[1]) + ph_change
            ph_data.append(ph)

            soil = int(data[2]) + random.randint(-10,8)
            soil_data.append(soil)

            light = int(data[3]) + random.randint(-5,5)
            light_data.append(light)

            

            counter += 1
        
        return temperature_data, ph_data, soil_data, light_data
         
class Posuda:

    def __init__(self, db_name) -> None:

        self.db_name = db_name
        
    def create_database(self):
        
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pot_data (
            id INTEGER PRIMARY KEY,
            Location TEXT NOT NULL,
            Plant_name TEXT NOT NULL,
            Soil_Humidity INTEGER NOT NULL,
            pH INTEGER NOT NULL,
            Temperature INTEGER NOT NULL,
            Light TEXT NOT NULL,
            Photo TEXT NOT NULL );

            """ 
        )  
        self.conn.close()

    def insert(self, Location, Plant_name, Soil_Humidity, pH, Temperature, Light, Photo):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO pot_data (Location, Plant_name, Soil_Humidity, pH, Temperature, Light, Photo) VALUES (?, ?, ?, ?, ?, ?, ?)",(Location, Plant_name, Soil_Humidity, pH, Temperature, Light, Photo,))
        self.conn.commit()
        self.conn.close()


    def name(self):

        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT Plant_name FROM pot_data")
        result = self.cursor.fetchone()
        self.conn.close()
        print(result)
        return result
    
    def remove(self, pot_table_id):

        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM pot_data WHERE id = ?",(pot_table_id,))
        self.conn.commit()
        self.conn.close()
        

    def update(self, location, plant_name,soil_hum, ph, temperature, light, photo_path, id):

        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute("UPDATE pot_data SET Location = ?, Plant_name = ?, Soil_Humidity = ?, pH = ?,Temperature = ?, Light = ?, Photo = ? WHERE id = ?",(location, plant_name, soil_hum, ph, temperature, light, photo_path, id))
        self.conn.commit()
        print("Updejtano 2")
        self.conn.close()



