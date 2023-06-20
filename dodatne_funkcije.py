from dbmanager.db_manager import *
from UserDataManipulation import *
from PlantDataManipulation import *
from Klase import *
from tkinter import END
from tkinter.filedialog import askopenfilename
import PIL.Image
import PIL.ImageTk
from tkinter import PhotoImage
from tkinter import ttk
import tkinter as tk
import os
from PotDataManipulation import Select_from_pot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox

Plants = Biljke("Plants.db")
password_visible = False

def Remove_plant_from_pot(id: str, location: str, middelLF: tk.LabelFrame, pot: tk.Tk):
    """Prazni posudu

    Args:
        id (str): id posude
        location (str): lokacija
        middelLF (tk.LabelFrame): Prikaz na glavnom ekranu aplikacije
        pot (tk.Tk): Podatci o posudi
    """
    plant_name = "Posuda prazna"
    soil_hum = "Posuda prazna"
    ph = "Posuda prazna"
    temperature = "Posuda prazna"
    light = "Posuda prazna"
    photo_path = "Slike\empty_pot.png"
    plant_remove = Posuda("Pots.db")
    plant_remove.update(location, plant_name,soil_hum, ph, temperature, light, photo_path, id)
    Pots(middelLF)
    pot.destroy()

def Data_comparison(data_comperison: tk.LabelFrame, plant_name: str, soil_hum:str, temperature: str, ph: str, light: str):
    """
    Usporedba i prikaz podataka sa senzora sa optimalnima
    Args:
        data_comperison (tk.LabelFrame): prikaz rezultata na ekranu
        plant_name (str): ime biljke
        soil_hum (str): vlažnost tla
        temperature (str): temperatura
        ph (str): pH
        light (str): svijetlost
    """
    try:
        optimal = Get_plant_data(plant_name)

    except:
        pass

    for widget in data_comperison.grid_slaves():
        widget.destroy()

    temp_comp = tk.Label(data_comperison)
    temp_comp.grid(row=0, column=0, padx=5, pady=5)

    ph_comp = tk.Label(data_comperison)
    ph_comp.grid(row=0, column=1, padx=5, pady=5)

    light_comp = tk.Label(data_comperison)
    light_comp.grid(row=0, column=2, padx=5, pady=5)

    hum_comp = tk.Label(data_comperison)
    hum_comp.grid(row=0, column=3, padx=5, pady=5)


    try: 
        if temperature < int(optimal[4]):
            temp_comp.config(text = "Temperatura: \nPosuda se nalazi u prehladnim uvijetima, \n premjestite posudu")
        elif temperature > int(optimal[5]):
            temp_comp.config(text = "Temperatura: \nPosuda se nalazi u pretoplim uvijetima, \n premjestite posudu")
        else:
            temp_comp.config(text = "Temperatura: \nPosuda se nalazi u idealnim uvijetima")

        if ph < int(optimal[6]-0.5) or ph > int(optimal[6]+0.5):     
            ph_comp.config(text = "pH tla ne odgovara ovoj biljci")
        else:
            ph_comp.config(text = "pH tla je idealan za ovu biljku")

        if soil_hum < int(optimal[2]-0.5):    
            hum_comp.config(text = "Biljka nema dovoljno vode")
        elif soil_hum > int(optimal[3]+0.5):  
            hum_comp.config(text = "Biljka ima previše vode")
        else:
            hum_comp.config(text = "Biljka je u idealnim uvjetima")
    
        if light < int(optimal[7]):
            light_comp.config(text = "Biljka nema dovoljno svijetla")
        else:
            light_comp.config(text= "Biljka ima dovoljno svijetla")

    except:
        pass

def Sync_data(subplot, canvas: FigureCanvasTkAgg, pot_label_hum: tk.Label,pot_temp_: str, pot_ph_: str, status: str, plant_name: str, subplot_3, canvas_3: FigureCanvasTkAgg, subplot_2, canvas_2: FigureCanvasTkAgg, pot_light_: str):
    """Ažurira podatke sa senzora

    Args:
        subplot (axes.Axes): osi grafa 1
        canvas (FigureCanvasTkAgg): graf temperature, ph i vlažnosti u vremenu
        pot_label_hum (tk.Label): Label koji prikazuje vlažnost
        pot_temp_ (tk.Label): label koji prikazuje temperatura sa senzora
        pot_ph_ (tk.Label): label koji prikazuj ph sa senzora
        status (str): status posude
        plant_name (str): ime biljke
        subplot_3 (axes.Axes): osi grafa 3
        canvas_3 (FigureCanvasTkAgg): graf postotka sati u optimalnim uvjetima temperature
        subplot_2 (axes.Axes): osi grafa 2
        canvas_2 (FigureCanvasTkAgg): graf vlažnosti u određenom satu
        pot_light_ (tk.Label): label koji prikazuj svijetlost sa senzora

    Returns:
        temperatura (str): nove temperatura sa senzoa
        ph (str): novi ph sa senzora
        vlažnost(str): nova vlažnost sa senzora
    """
   
    if status == "Aktivna":
        subplot.clear()

        data = Senzor.get_senzor_data()
        pH = data[1]
        Soil = data[2]
        x = [1,2,3,4,5,6,7,8,9,10,11,12]
        temperatura = data[0]

        
        subplot.plot(x, temperatura, label = "Temperatura")
        subplot.plot(x, pH, label = "pH")
        subplot.plot(x, Soil, label = "Humidity")
        subplot.legend(loc = "lower right", fontsize = "7")
        canvas.draw()

        pot_label_hum.config(text = data[2][len(data)])
        pot_temp_.config(text = data[0][len(data)])
        pot_ph_.config(text = data[1][len(data)])
        pot_light_.config(text = data[3][len(data)])

        subplot_3.clear()
        optimal = Get_plant_data(plant_name)
        temperature_value_min = optimal[4]
        temperature_value_max = optimal[5]

        optimal_conditions = 0
        total_measurements = 0

        for value in data[0]:
            if value < temperature_value_min or value > temperature_value_max:
                total_measurements += 1
            else:
                optimal_conditions += 1
                total_measurements += 1

        optimal_percentage = (optimal_conditions/total_measurements)*100
        labels = ["Sati u optimalnim uvjetima","Sati van optimalnih uvjeta"]
        sizes = [optimal_percentage,100-optimal_percentage]

        subplot_3.pie(sizes, autopct='%1.1f%%')
        subplot_3.legend(labels, loc = "lower right", fontsize = "7")
        
        canvas_3.draw()

        subplot_2.clear()

        humidity_data = []
        for i in data[2]:
            humidity_data.append(i)
            number_of_measurments =[i for i in range(1, len(humidity_data)+1)]

        subplot_2.bar(number_of_measurments,humidity_data)
        canvas_2.draw()

        return temperatura, pH, Soil
    else:
        messagebox.showinfo("","Posuda trenutno nije aktivna")
 
def Pots(middelLF: tk.LabelFrame):
    """Provjerava postoje li posude u bazi podataka, te na osnovu tog kreira dugmad.

    Args:
        middelLF (tk.LabelFrame): dio GUIa u kojemu se prikazuju dugmad.
    """
    try:
        pots = Select_from_pot()

        for rows in pots:
            plant = rows[2]
            if plant == "Posuda prazna" or plant == None:
                pot_status = "Posuda prazna"
            else:
                pot_status = "Aktivna"
            id = rows[0]
            location = rows[1]
            pot_button = tk.Button(middelLF,width=11, height=5, text=f"{id} {location} \n {pot_status}", command=lambda id = id, status = pot_status: Pot_details(id, middelLF, status))
            row = (id - 1)//3
            column = (id - 1) % 3

            pot_button.grid(row = row, column=column, padx=5, pady=5)
    except:
        pass
            
def Change_plant(pot: tk.Tk, location: str, id: str, plant_name: str, optimal_temperature_show: str, optimal_ph_show: str, optimal_hum_show: str, pot_frame: tk.LabelFrame, picture: str):
    """Mijenja biljku u posudi

    Args:
        pot (tk.Tk): Glavni ekran u kojem se pokazuju podatci o posudi
        location (str): lokacija posude
        id (str): id posude
        plant_name (str): ime biljke trenutno u posudi
        optimal_temperature_show (str): optimalna temperatura
        optimal_ph_show (str): optimalni pH
        optimal_hum_show (str): optimalna vlažnost
        pot_frame (tk.LabelFrame): Label frame u kojemu se nalaze informacije o posudi
        picture (str): putanja do slike biljke
    """
    
    optimal = Get_plant_data(plant_name)
    picture.destroy()
    
    photo_path = f"{optimal[8]}"
    picture = PIL.ImageTk.PhotoImage(master = pot_frame, image = PIL.Image.open(photo_path, "r"))
    plant_picture = tk.Label(pot_frame, image=picture)
    plant_picture.photo = picture
    picture = PhotoImage(master=plant_picture)
    plant_picture.grid(row=0, column=0, rowspan=3, columnspan=3)
    temperature = optimal[4]
    soil_humidity = optimal[2]
    ph = optimal[3]
    light = optimal[5]
    change_plant = Posuda("Pots.db")
    change_plant.update(location, plant_name, soil_humidity, temperature, ph, light, photo_path, id)
    
    

    optimal_temperature_show.config(text = f"{optimal[4]}-{optimal[5]}" )
    optimal_ph_show.config(text=f"{optimal[6]-0.5}-{optimal[6]+0.5}")
    optimal_hum_show.config(text=f"{optimal[2]}-{optimal[3]}")

    pot.destroy()

def Pot_details(id: str, middelLF: tk.LabelFrame, status: str):
    """prikazuju se podatci o posudi

    Args:
        id (str): id posude
        middelLF (tk.LabelFrame): Dio aplikacije u kojemu se prikazuju posude
        status (str): status posude Aktivna/Prazna
    """

    pot = tk.Tk()
    pot.title("Posude")
    pot_frame = tk.LabelFrame(pot, text=f"Posuda broj: {id}")
    pot_frame.pack()

    pots = Select_from_pot()
    if status == "Aktivna":
        data = Senzor.get_senzor_data()
    else:
        data = ["Prazna posuda","Prazna posuda","Prazna posuda"]
 

    for row in pots:
        if row[0] == id:
            id = row[0]
            location = row[1]
            plant_name = row[2]
            if status == "Aktivna":
                soil_hum = data[2][len(data)]
                ph = data[1][len(data)]
                temperature = data[0][len(data)]
                light = data[3][len(data)]
            else:
                soil_hum = data[2]
                ph = data[1]
                temperature = data[0]
                light = row[0]
            photo_path = f"{row[7]}"
            picture = PIL.Image.open(photo_path, "r")
            size = (200,200)
            resize_picture = picture.resize(size)
            picture = PIL.ImageTk.PhotoImage(master = pot_frame, image = resize_picture)
            plant_picture = tk.Label(pot_frame, image=picture)
            plant_picture.photo = picture
            picture = PhotoImage(master=plant_picture)
            plant_picture.grid(row=0, column=0, rowspan=3, columnspan=3)
    
            pot_location_label = tk.Label(pot_frame, text="Lokacija posude: ")
            pot_location_label.grid(row=0, column=4)
            pot_location_entry = tk.Entry(pot_frame)
            pot_location_entry.grid(row=0, column=5)
            pot_location_entry.insert(tk.END, location)
            pot_name_label = tk.Label(pot_frame, text="Trenutna biljka:  ")
            pot_name_label.grid(row=1, column=4, padx=5, pady=5)

            plant = Select_Data_From_Database()

            option_list = []
            for row in plant:
                if row == False:
                    continue
                else:
                    Name = row[1]
                    option_list.append(Name)

            try:
                optimal = Get_plant_data(plant_name)
                
            except:
                optimal = ["Prazna posuda","Prazna posuda","Prazna posuda","Prazna posuda","Prazna posuda","Prazna posuda","Prazna posuda",]

            current_plant = plant_name
            selected_option = tk.StringVar(pot_frame)     
            selected_option.set(f"{current_plant}")
            
    
            pot_hum_label = tk.Label(pot_frame, text="Trenutna vlažnost tla (%): ")
            pot_hum_label.grid(row=2, column=4, padx=5, pady=5)
            pot_label_hum = tk.Label(pot_frame, text = f"{soil_hum}")
            pot_label_hum.grid(row=2, column=5, padx=5, pady=5)

            optimal_humidity = tk.Label(pot_frame, text="Optimalna vlažnost tla (%): ")
            optimal_humidity.grid(row=2, column = 6, padx=5, pady=5)

            if status == "Aktivna":
                optimal_hum_show = tk.Label(pot_frame, text=f"{optimal[2]}-{optimal[3]}")
                optimal_hum_show.grid(row=2, column = 7, padx = 5, pady=5)
            else:
                optimal_hum_show = tk.Label(pot_frame, text=f"Prazna posuda")
                optimal_hum_show.grid(row=2, column = 7, padx = 5, pady=5)


            pot_temp_label = tk.Label(pot_frame, text="Trenutni pH: ")
            pot_temp_label.grid(row=3, column=4, padx=5, pady=5)
            pot_ph_ = tk.Label(pot_frame, text = f"{ph}")
            pot_ph_.grid(row=3, column=5, padx=5, pady=5)

            
            optimal_ph = tk.Label(pot_frame, text = "Optimalni pH: ")
            optimal_ph.grid(row=3, column=6, padx=5, pady=5)

            if status == "Aktivna":
                optimal_ph_show = tk.Label(pot_frame, text=f"{optimal[6]-0.5}-{optimal[6]+0.5}")
                optimal_ph_show.grid(row=3, column=7)
            else:
                optimal_ph_show = tk.Label(pot_frame, text=f"Prazna posude")
                optimal_ph_show.grid(row=3, column=7)
        
            pot_temp_label = tk.Label(pot_frame, text="Trenutna temperatura (°C): ")
            pot_temp_label.grid(row=4, column=4, padx=5, pady=5)

            pot_temp_ = tk.Label(pot_frame, text = f"{temperature}")
            pot_temp_.grid(row=4, column=5, padx=5, pady=5)

            optimal_temperature = tk.Label(pot_frame, text="Optimalna temperatura: ")
            optimal_temperature.grid(row=4, column=6, padx=5, pady=5)

            optimal_light = tk.Label(pot_frame, text="Optimalna svijetlost: ")
            optimal_light.grid(row = 5, column=6)

            if status == "Aktivna":
                optimal_temperature_show = tk.Label(pot_frame, text = f"{optimal[4]}-{optimal[5]}")
                optimal_temperature_show.grid(row=4, column=7, padx=5, pady=5)
            else:
                optimal_temperature_show = tk.Label(pot_frame, text = f"Prazna posuda" )
                optimal_temperature_show.grid(row=4, column=7, padx=5, pady=5)

            pot_light_label = tk.Label(pot_frame, text="Trenutno osvijetljenje: ")
            pot_light_label.grid(row=5, column=4, padx=5, pady=5)
            pot_light_ = tk.Label(pot_frame, text = f"{light}")
            pot_light_.grid(row=5, column=5, padx=5, pady=5)

            if status == "Aktivna":
                optimal_light_show = tk.Label(pot_frame, text = f"{optimal[7]}")
                optimal_light_show.grid(row=5, column=7, padx=5, pady=5)
            else:
                optimal_light_show = tk.Label(pot_frame, text = f"Prazna posuda" )
                optimal_light_show.grid(row=5, column=7, padx=5, pady=5)

            option_menu = ttk.OptionMenu(pot_frame, selected_option,f"{current_plant}", *option_list)
            option_menu.grid(row=1, column=5) 

            data_comperison = tk.LabelFrame(pot, text="Uvjeti")
            data_comperison.pack()

            try:
                Data_comparison(data_comperison, plant_name, soil_hum, temperature, ph, light)

            except:
                pass

            graphs_FL = tk.LabelFrame(pot, text="Podatci sa senzora")
            graphs_FL.pack()
            
            temperature_over_time = Figure(figsize=(5, 3), dpi=100)
            subplot = temperature_over_time.add_subplot(111)

            if row == False:
                continue
            else:
                data = Senzor.get_senzor_data()
            y1 = data[0]
            y2 = data[1]
            y3 = data[2]
    
            x = [1,2,3,4,5,6,7,8,9,10,11,12]
            subplot.plot(x, y1, label = "Temperatura")
            subplot.plot(x, y2, label = "pH")
            subplot.plot(x, y3, label = "Humidity")
            subplot.legend(loc = "lower right", fontsize = "5")
            canvas = FigureCanvasTkAgg(temperature_over_time, master=graphs_FL)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)
            subplot.set_xlabel("Vrijeme /h")  
            subplot.set_ylabel("Vrijednost")  

            fig_2= Figure(figsize=(5, 3), dpi=100)
            subplot_2 = fig_2.add_subplot(111)
            humidity_data = []
            for i in data[2]:
                humidity_data.append(i)
            number_of_measurments =[i for i in range(1, len(humidity_data)+1)]
            subplot_2.bar(number_of_measurments,humidity_data)
            subplot_2.set_xlabel("Dani")
            subplot_2.set_ylabel("Postotak vlaznosti")
            
            canvas_2 = FigureCanvasTkAgg(fig_2, master=graphs_FL)
            canvas_2.draw()
            canvas_2.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)
    
            temperature_value_min = optimal[4]
            temperature_value_max = optimal[5]
    
            optimal_conditions = 0
            total_measurements = 0

            try: 
                for value in data[0]:
                    if value < temperature_value_min or value > temperature_value_max:
                        total_measurements += 1
                    else:
                        optimal_conditions += 1
                        total_measurements += 1

                optimal_percentage = (optimal_conditions/total_measurements)*100
            except:
                pass
       
            try: 
                fig_3 = Figure(figsize=(5, 3), dpi=100)
                subplot_3 = fig_3.add_subplot(111)
                labels = ["Sati u optimalnim uvjetima","Sati van optimalnih uvjeta"]
                sizes = [optimal_percentage,100-optimal_percentage]
                subplot_3.pie(sizes,autopct='%1.1f%%')
                subplot_3.legend(labels, loc = "lower right", fontsize = "7")
                canvas_3 = FigureCanvasTkAgg(fig_3, master=graphs_FL)
                canvas_3.draw()
                canvas_3.get_tk_widget().grid(row = 0, column = 2, padx=5, pady=5)
            except:
                canvas_3 = ""

            buttons_FL = tk.LabelFrame(pot)
            buttons_FL.pack()

            update_pot = tk.Button(buttons_FL, text="Ažuriraj posudu", command= lambda: (Change_plant(pot, pot_location_entry.get(), id, selected_option.get(), optimal_temperature_show, optimal_ph_show, optimal_hum_show, pot_frame, plant_picture), Pots(middelLF)))
            update_pot.grid(row=0, column=0, padx=5, pady=5)

            delete_pot = tk.Button(buttons_FL, text="Isprazni posudu", command=lambda:Remove_plant_from_pot(id, location, middelLF, pot))
            delete_pot.grid(row=0, column=1, padx=5, pady=5)

            return_button = tk.Button(buttons_FL, text="Odustani", command=lambda: pot.destroy())
            return_button.grid(row = 0, column=2, padx=5, pady=5)

            sync_button = tk.Button(buttons_FL, text="Sinkroniziraj", command=lambda:(Sync_data(subplot, canvas, pot_label_hum, pot_temp_, pot_ph_, status, plant_name, subplot_3, canvas_3, subplot_2, canvas_2, pot_light_),  Data_comparison(data_comperison, plant_name, pot_label_hum.cget("text"), pot_temp_.cget("text"), pot_ph_.cget("text"), pot_light_.cget("text"))))
            sync_button.grid(row=0, column=3, padx=5, pady=5)

def Add_plant_to_pot(plant: str, screen: tk.LabelFrame, location: str, pot_number: str, new_pot_screen: tk.Tk):
    """Dodaje biljku u posudu

    Args:
        plant (str): ime biljke
        screen (tk.LabelFrame): prikaz posude na ekranu
        location (str): lokacija posude
        pot_number (str): broj posude
        new_pot_screen (tk.Tk): prozor u kojemu se biljka dodaje u posudu
    """
    new_pot_screen.destroy()
    temperature = Senzor.Temperatura()
    soil_humidity = Senzor.Soil_humidity()
    pH = Senzor.pH()
    light = Senzor.light()

    plants = Select_Data_From_Database()
    paths = []
    plant_names = []
    plant_dict={}
    for rows in plants:
        plant_name = rows[1]
        path = rows[8]
        paths.append(path)
        plant_names.append(plant_name)
    
    for i in range(len(plant_names)):
        key = plant_names[i]
        value = paths[i]
        plant_dict[key] = value
    

    path = plant_dict[plant]
    
    row = (pot_number - 1) // 3
    column = (pot_number - 1) % 3
    new_pot = Posuda(f"Pots.db")
    new_pot.create_database()
    new_pot.insert(location,plant,soil_humidity,pH,temperature,light,path)
    new_pot_button = tk.Button(screen, width=11, height=5, text=f"{pot_number} {location} \nAktivna", command= lambda: Pot_details(pot_number, screen, status="Aktivna"))
    new_pot_button.grid(row=row, column=column, padx=5, pady= 5)
       
def Select(plant_name_get: tk.Label, value: str):
    """Izmjena biljke

    Args:
        plant_name_get (tk.Label): Label u kojemu se mijenja tekst
        value (str): novi tekst
    """
    plant_name_get.config(text = value)

def Edit_plant_data(plant_list: ttk.Treeview, name_entry: str, minHum_entry: str, maxHum_entry: str, minTemp_entry: str, maxTemp_entry: str, ph_entry: str, light_entry: str):
    """_promjena podataka o biljci

    Args:
        plant_list (ttk.Treeview): prikaz tablice
        plant_info (tk.Label): label s informacijama o biljci
        panel (tk.Label): label sa fotografijom
        name_entry (str): ime biljke
        minHum_entry (str): minimalna vlažnost
        maxHum_entry (str): maksimalna vlažnost
        minTemp_entry (str): minimalna temperatura
        maxTemp_entry (str): maksimalna temperatura
        pH_entry (str): ph
        light_entry (str): svijetlost
        light_entry (str): _description_
    """
    id = ID_plant(name_entry)
    Change_plant_data(name_entry, minHum_entry, maxHum_entry, minTemp_entry, maxTemp_entry,ph_entry, light_entry, id)
    update_plant_list(plant_list)

def Upload_file(photo_entry: str):
    """Dodaje putanju slike

    Args:
        photo_entry (str): putanja slike

    Returns
        filepath (str): putanja slike
    """
    f_types = [("Jpg files", "*jpg"), ("PNG files","*png")]
    filename = tk.filedialog.askopenfilename(filetypes = f_types)
    if filename:
        base_directory = r"C:/Users/Sime/Desktop/Seminar"
        filepath = os.path.abspath(filename)
        relative_path = os.path.relpath(filepath, base_directory)
        print(relative_path)
        photo_entry.insert(tk.END, relative_path)

    

    return filepath

def Select_item(plant_list: ttk.Treeview, plant_info: tk.Label, panel: tk.Label, name_entry: str, minHum_entry:str, maxHum_entry: str, minTemp_entry:str, maxTemp_entry:str, pH_entry: str, light_entry:str):
    """Biranje biljke za prikaz

    Args:
        plant_list (ttk.Treeview): prikaz tablice
        plant_info (tk.Label): label s informacijama o biljci
        panel (tk.Label): label sa fotografijom
        name_entry (str): ime biljke
        minHum_entry (str): minimalna vlažnost
        maxHum_entry (str): maksimalna vlažnost
        minTemp_entry (str): minimalna temperatura
        maxTemp_entry (str): maksimalna temperatura
        pH_entry (str): ph
        light_entry (str): svijetlost

    Returns:
        id(str): id biljke
    """
    try:

        curItem = plant_list.focus()
        dict = (plant_list.item(curItem))
        values = dict["values"]

        id = values[0]

        name_entry.config(text = f"{values[1]}")

        minHum_entry.delete(0,END)
        minHum_entry.insert(0, f"{values[2]}%")

        maxHum_entry.delete(0,END)
        maxHum_entry.insert(0, f"{values[3]}%")

        minTemp_entry.delete(0,END)
        minTemp_entry.insert(0, f"{values[4]}°C")

        maxTemp_entry.delete(0,END)
        maxTemp_entry.insert(0, f"{values[5]}°C")

        pH_entry.delete(0, END)
        pH_entry.insert(0, f"{values[6]}")

        light_entry.delete(0,END)
        light_entry.insert(0, f"{values[7]}")
        
        data = Select_Data_From_Database()
        photo_paths = []
        for row in data:
            photo_paths.append(row[8])
    
        path = f"{photo_paths[id-1]}"
        size = (200,200)
        img = PIL.Image.open(path)
        resized_img = img.resize(size)
        img = PIL.ImageTk.PhotoImage(master = plant_info, image = resized_img)
        
        panel = tk.Label(plant_info, image=img)
        panel.photo = img
        panel.grid(column=0,row=0)
        
        return id
    
    except IndexError as e:
        pass

def Update_entry(Username_entry: tk.Entry, Password_entry:tk.Entry, id: str):
    """Mijenja unose u entry-u

    Args:
        Username_entry (tk.Entry): _description_
        Password_entry (tk.Entry): _description_
        id (str): _description_
    """

    username = get_new_username(id)
    password = get_new_password(id)

    Username_entry.delete(0, 'end')
    Password_entry.delete(0, 'end')
    
    Username_entry.insert(0, username)
    Password_entry.insert(0, password)
    
def update_upperlf_text(upperLF: tk.LabelFrame, username: str, password: str):
    """Mjenja naziv labelframea

    Args:
        upperLF (tk.LabelFrame): Label frame
        username (str): korisničko ime
        password (str): lozinka
    """
    name_lable = Update_username(username, password)
    upperLF.configure(text=name_lable)
    upperLF.after(1000, lambda: update_upperlf_text(upperLF, username, password))

def Delete_plant(plant_list: ttk.Treeview, name_entry: tk.LabelFrame):

    """Briše biljku iz baze podatka
    Args:
        plant_list (ttk.Treeview): prikaz tablice
        name_entry (tk.LabelFrame): ime biljke

    """
    
    id = ID_plant(name_entry.cget("text"))
    Plants.remove(id)
    
    update_plant_list(plant_list)

def Show_password(Password_entry: tk.Entry):
    """prikaz lozinke
    Args:
        Password_entry (tk.Entry): str

    Returns:
        Password_entry (tk.Entry): str
    """
    global password_visible
    password_visible = not password_visible
    show_char = "" if password_visible else "*"
    Password_entry = Password_entry.config(show=show_char)
    return Password_entry

def Create_user_table(username: str, ID: str):
    """
    Stvara bazu podataka za trenutnog korisnika

    username(str): korisničko ime
    ID(str): id broj
    """
    db_file = "Current_User.db"

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Current_User (
        id INTEGER PRIMARY KEY,
        Username TEXT NOT NULL,
        database_ID TEXT NOT NULL
    );
    """
    insert_into_table_sql = """
        INSERT INTO Current_User (Username, database_ID)
        VALUES (?, ?);
        """
    

    sql_connection = create_connection(db_file)
    success = create_table(sql_connection, create_table_sql)
    if success:
        print("Uspjesno smo napravili tablicu")
    else:
        print("Nismo napravili tablicu")

    data = [(username, ID)]
        
    success = insert_into_table(sql_connection, insert_into_table_sql, data)
    if success:
        print("Uspjesno smo dodali podatke u tablicu")
    else:
        print("Nismo dodali podatke u tablicu")

def Update_username(username: str, password: str):
    """
    Ažurira korisničko ime
    Args:
        username (str): korisničko ime
        password (str): lozinka

    Returns:
        _updated_username(str): promjenjeno korisničko ime
    """

    database_ID = ID_current("Current_User.db", username, password)
    updated_username = return_username(database_ID)
    updated_username = updated_username[0]

    return updated_username

def get_new_username(id: str):
    """vraća novo korisničko ime

    Args:
        id (str): id

    Returns:
        new_username(str): novo korisničko ime
    """
    new_username = return_username(id)
    return new_username

def get_new_password(id: str):
    """vraća novu lozinku

    Args:
        id (str): id

    Returns:
        new_password: nova lozinka
    """
    new_password = return_password(id)
    return new_password

def update_plant_list(plant_list: ttk.Treeview):
    """Ažurira listu biljki

    Args:
        plant_list (ttk.Treeview): Lista biljki
    """

    Plant_list = Select_Data_From_Database()
    plant_list.delete(*plant_list.get_children())

    for number,row in enumerate(Plant_list, 1):
        if row == False:
            continue
        else:
            Broj = number
            Name = row[1]
            minHum = row[2]
            maxHum = row[3]
            minTemp = row[4]
            maxTemp = row[5]
            light = row[6]
            photo = row[7]
            plant_list.insert(parent = "", index = "end", values =(Broj,Name, minHum, maxHum, minTemp, maxTemp, light, photo))

def Save(plant_list: ttk.Treeview,Name:str, minHum: str, maxHum: str, minTemp: str, maxTemp: str, pH: str, light: str, photo: str):
    """Upisuje novu biljku u bazu podataka

    Args:
        plant_list (ttk.Treeview): tablica koja prikazuje biljke
        Name (str): Ime biljke
        minHum (str): minimalna vlažnost
        maxHum (str): maximalna vlažnost
        minTemp (str): minimalna temperatura
        maxTemp (str): mahimalna temperatura
        pH (str): optimalni ph
        light (str): optimalna svijetlost
        photo (str): putanja fotografije
    """

    try:
        db = Biljke("Plants.db")
        db.insert(Name, minHum, maxHum, minTemp, maxTemp, pH, light, photo)

        update_plant_list(plant_list)
    except IndexError:
        pass
