import tkinter as tk
from tkinter import *
from tkinter import messagebox
from UserDataManipulation import *
from dodatne_funkcije import *
from tkinter import ttk
from Klase import *
from tkinter.filedialog import askopenfilename
from PotDataManipulation import *
from temperatura_API import *

def New_pot_screen(screen: tk.Tk):
    """Stvara ekran za stvaranje nove posude

    Args:
        screen (tk.Tk): grafički prikaz
    """
    pot_number = Database_len()

    if type(pot_number) == tuple:
        pot_number = pot_number[0]+1
    else:
        pot_number =+ 1

    new_pot_screen = tk.Tk()
    new_pot_screen.title("Nova posuda")

    pot_information = tk.LabelFrame(new_pot_screen)
    pot_information.pack()

    plant_name = tk.Label(pot_information, text="Biljka u posudi: ")
    plant_name.grid(row=0, column=0)

    plant_name_get = tk.Label(pot_information, text="\t\t")
    plant_name_get.grid(row=0, column=1)
    
    new_pot_LF = tk.LabelFrame(new_pot_screen, text="Dodajte novu posudu")
    new_pot_LF.pack()
    
    pot_ID = tk.Label(new_pot_LF, text="Broj posude")
    pot_ID.grid(column=0, row=0)

    ID_number = tk.Label(new_pot_LF, text=f"{pot_number}")
    ID_number.grid(column = 1, row= 0)
    
    option_menu_label = tk.Label(new_pot_LF, text="Odaberite biljku: ")
    option_menu_label.grid(row=2, column=0)

    pot_location = tk.Label(new_pot_LF, text = "Upišite lokaciju biljke: ")
    pot_location.grid(row=1, column=0)

    pot_location_entry = tk.Entry(new_pot_LF)
    pot_location_entry.grid(row = 1, column=1)
    
    plant = Select_Data_From_Database()

    option_list = []
    for row in plant:
        if row == False:
            continue
        else:
            Name = row[1]
            option_list.append(Name)

    selected_option = tk.StringVar(new_pot_LF)     
    selected_option.set("Odaberi biljku")
    option_menu = ttk.OptionMenu(new_pot_LF, selected_option,"Odaberi biljku", *option_list, command=lambda value :Select(plant_name_get, value))
    option_menu.grid(row=2, column=1) 

    add_plant_to_pot = tk.Button(new_pot_LF, text="Dodaj biljku u posudu", command=lambda:Add_plant_to_pot(plant_name_get.cget("text"), screen, pot_location_entry.get(), pot_number, new_pot_screen))
    add_plant_to_pot.grid(row=3, column=1, padx=5, pady=5)
    
    return_button = tk.Button(new_pot_LF, text="Odustani", command= lambda: new_pot_screen.destroy())
    return_button.grid(row = 3, column= 2)

def New_plant(plant_list: ttk.Treeview):
    """Stvara ekran za dodavanje nove biljke

    Args:
        plant_list (ttk.Treeview): Popis biljki
    """
    new_plant = tk.Tk()
    new_plant.title("Nova biljka")

    new_plant_LF = tk.LabelFrame(new_plant, text="Unesite podatke o biljci")
    new_plant_LF.pack(padx=5, pady=5)

    Name_label = tk.Label(new_plant_LF,text="Naziv biljke: ")
    Name_entry = tk.Entry(new_plant_LF)
    Name_label.grid(row=0, column=0)
    Name_entry.grid(row=0, column=1)

    minHum_label = tk.Label(new_plant_LF,text="Minimalna vlažnost: ")
    minHum_entry = tk.Entry(new_plant_LF)
    minHum_label.grid(row=1, column=0)
    minHum_entry.grid(row=1, column=1)

    maxHum_label = tk.Label(new_plant_LF,text="Maximalna Vlažnost: ")
    maxHum_entry = tk.Entry(new_plant_LF)
    maxHum_label.grid(row=2, column=0)
    maxHum_entry.grid(row=2, column=1)

    minTemp_label = tk.Label(new_plant_LF,text="Minimalna Temperatura: ")
    minTemp_entry = tk.Entry(new_plant_LF)
    minTemp_label.grid(row=3, column=0)
    minTemp_entry.grid(row=3, column=1)

    maxTemp_label = tk.Label(new_plant_LF,text="Maximalna Temperatura: ")
    maxTemp_entry = tk.Entry(new_plant_LF)
    maxTemp_label.grid(row=4, column=0)
    maxTemp_entry.grid(row=4, column=1)

    pH_label = tk.Label(new_plant_LF,text="Optimalni pH: ")
    pH_entry = tk.Entry(new_plant_LF)
    pH_label.grid(row=5, column=0)
    pH_entry.grid(row=5, column=1)

    light_label = tk.Label(new_plant_LF,text="Svijetlost: ")
    light_entry = tk.Entry(new_plant_LF)
    light_label.grid(row=6, column=0)
    light_entry.grid(row=6, column=1)

    photo_label = tk.Label(new_plant_LF,text="Fotografija: ")
    photo_entry = tk.Entry(new_plant_LF)
    photo_label.grid(row=7, column=0)
    photo_entry.grid(row=7, column=1,)
    photo_button = tk.Button(new_plant_LF, text="Učitajte sliku", command=lambda: Upload_file(photo_entry))
    photo_button.grid(row=8, column= 1)

    buttons = tk.LabelFrame(new_plant,text = "Opcije")
    save_button = tk.Button(buttons, text="Spremi", command=lambda: Save(plant_list, Name_entry.get(),minHum_entry.get(),maxHum_entry.get(),minTemp_entry.get(),maxTemp_entry.get(),pH_entry.get(),light_entry.get(),photo_entry.get()))
    return_button = tk.Button(buttons, text="Odustani", command=lambda: new_plant.destroy())

    buttons.pack()
    save_button.grid(row=0, column=0, padx=5, pady=5)
    return_button.grid(row=0, column=1, padx=5, pady=5)
  
def Plant_list():

    Plants = tk.Tk()
    Plants.title("Biljke")

    plant_list = ttk.Treeview(Plants)
    plant_list["columns"] = ("Broj", "Naziv", "Minimalna Vlažnost", "Maximalna Vlažnost", "Minimalna Temperatura", "Maximalna Temperatura","pH","Svijetlost","Fotografija")

    plant_list.column("#0",width=0,stretch="NO")
    plant_list.column("Broj",width=50, anchor="center")
    plant_list.column("Naziv",width=80, anchor="center")
    plant_list.column("Minimalna Vlažnost",width=180, anchor="center")
    plant_list.column("Maximalna Vlažnost",width=180, anchor="center")
    plant_list.column("Minimalna Temperatura",width=180, anchor="center")
    plant_list.column("Maximalna Temperatura",width=180, anchor="center")
    plant_list.column("pH", width=50, anchor="center" )
    plant_list.column("Svijetlost",width=100, anchor="center")
    
    plant_list.heading("Broj",text = "Broj",anchor="center")
    plant_list.heading("Naziv",text = "Naziv",anchor="center")
    plant_list.heading("Minimalna Vlažnost",text ="Minimalna Vlažnost",anchor="center")
    plant_list.heading("Maximalna Vlažnost",text ="Maximalna Vlažnost",anchor="center")
    plant_list.heading("Minimalna Temperatura",text ="Minimalna Temperatura",anchor="center")
    plant_list.heading("Maximalna Temperatura",text ="Maximalna Temperatura",anchor="center")
    plant_list.heading("pH", text="pH", anchor="center")
    plant_list.heading("Svijetlost",text = "Svijetlost",anchor="center")

    plant_info = tk.LabelFrame(Plants, text = "Informacije o biljkama")
    
    plant_list.pack(padx=5, pady=5)
    plant_info.pack(padx=5, pady=5)

    panel = tk.Label(plant_info, image=None)
    panel.grid(column=0,row=0)

    info = tk.LabelFrame(plant_info)
    info.grid(column=1, row=0)

    name_label = tk.Label(info, text="Naziv: ")
    name_label.grid(row=0, column=0)
    name_entry = tk.Label(info, text = "")
    name_entry.grid(row=0, column=1)

    minHum_label = tk.Label(info, text="Minimalna vlažnost: ")
    minHum_label.grid(row=1, column=0)
    minHum_entry = tk.Entry(info)
    minHum_entry.grid(row=1, column=1)

    maxHum_label = tk.Label(info, text="Maximalna vlažnost: ")
    maxHum_label.grid(row=2, column=0)
    maxHum_entry = tk.Entry(info)
    maxHum_entry.grid(row=2, column=1)

    minTemp_label = tk.Label(info,text = "Minimalna temperatura: ")
    minTemp_label.grid(row=3, column=0)
    minTemp_entry = tk.Entry(info)
    minTemp_entry.grid(row=3, column=1)

    maxTemp_label = tk.Label(info,text = "Maximalna temperatura: ")
    maxTemp_label.grid(row=4, column=0)
    maxTemp_entry = tk.Entry(info)
    maxTemp_entry.grid(row=4, column=1)

    light_label = tk.Label(info, text="Svijetlost: ")
    light_label.grid(row=5, column=0)
    light_entry = tk.Entry(info)
    light_entry.grid(row=5, column=1)

    ph_label = tk.Label(info, text="Optimalni pH: ")
    ph_label.grid(row=6, column=0)
    ph_entry = tk.Entry(info)
    ph_entry.grid(row=6, column=1)
    
    plant_list.bind("<ButtonRelease-1>", lambda event:Select_item(plant_list, plant_info, panel, name_entry, minHum_entry, maxHum_entry, minTemp_entry, maxTemp_entry,ph_entry, light_entry))
    
    edit_plant_data = tk.Button(info, text="Uredi", command=lambda: Edit_plant_data(plant_list, name_entry.cget("text"), minHum_entry.get(), maxHum_entry.get(), minTemp_entry.get(), maxTemp_entry.get(), ph_entry.get(), light_entry.get()))
    edit_plant_data.grid(row = 7, column= 1)

    buttons = tk.LabelFrame(Plants,text = "Opcije")
    new_plant_button = tk.Button(buttons, text="Nova Biljka", command=lambda: New_plant(plant_list))
    return_button = tk.Button(buttons, text="Odustani", command=lambda: Plants.destroy())
    delete_plant = tk.Button(buttons, text = "Izbriši biljku", command=lambda:Delete_plant(plant_list, name_entry))

    buttons.pack()
    new_plant_button.grid(row=0, column=0, padx=5, pady=5)
    return_button.grid(row=0, column=1, padx=5, pady=5)
    delete_plant.grid(row=0, column=3, padx=5, pady=5)

    update_plant_list(plant_list)
   
def Log_out(main_app: Tk):
    """
    Odjavljuje korisnika iz aplikacije
    Args:
        main_app (Tk): Screen
    """

    delete_current_user()
    main_app.destroy()
    First_screen()
    
def First_screen():
    """
    Početni screen aplikacije
    """
    root = tk.Tk()
    root.title("PyPlant")
    
    main_label = tk.LabelFrame(root)
    main_label.pack(expand = True, anchor=tk.CENTER)
    Sign_up_button = tk.Button(main_label, text="Registrirajte novog korisnika", width=25, command=lambda: (Sign_in_screen(), root.destroy()))
    Sign_up_button.grid(pady = 5, padx= 5, column=0, row=0)
    Log_in_Button = tk.Button(main_label, text="Prijavi se", command=lambda: (Log_in_screen(), root.destroy()))
    Log_in_Button.grid(pady = 5,padx= 5, column=0, row=1,sticky="ew")
    root.mainloop()

def Main_app(username: str, password: str):

    """
    Pokreće se glavni dio aplikacije
    Args:
        username: str
        password: str

    """
    main_app = tk.Tk()
    main_app.title("PyPlant")

    upperLF = tk.LabelFrame(main_app, text=username, width=300, height=100)
    update_upperlf_text(upperLF, username, password)
    middelLF = tk.LabelFrame(main_app, width=300, height=400) 
    lowerLF = tk.LabelFrame(main_app, width=300, height=40)
    upperLF.grid_propagate(0)
    upperLF.pack(padx=5, pady=5)
    middelLF.grid_propagate(0)
    middelLF.pack(padx=5, pady=5)
    lowerLF.grid_propagate(0)
    lowerLF.pack(padx=5, pady=5) 

    #Gornja trećina
    options = ["Uredi", "Odjava"]
    selected_option = tk.StringVar()
    selected_option.set(username)
    option_menu = tk.OptionMenu(upperLF,selected_option, *options, command= lambda selection:(Edit_data_screen(username, password) if selection == "Uredi" else Log_out(main_app)))
    option_menu.place(relx= 0, rely=0.05, anchor="nw")

    Plants = tk.Button(upperLF, text = "Biljke", command=Plant_list)
    Plants.place(relx= 0.5, rely=0.05, anchor="n")

    temperature_value = get_current_temperature()
    temperature = tk.Label(upperLF, text=temperature_value)
    temperature.place(relx= 0.95, rely=0.05, anchor="ne")

    #Srednja trećina

    Pots(middelLF)

    #Donja trećina

    new_pot_button = tk.Button(lowerLF, text="Nova posuda", command=lambda: New_pot_screen(middelLF))
    new_pot_button.pack(padx=5, pady=5)
   
def Errot_Screen(text:str):

    """
    Prikazuje grešku, ukoliko je unesena kriva kombinacija korisničkog imena i lozinke, te ponovno prikazuje log in screen
    Args:
        text(str): error text
    """
    messagebox.showinfo("",text)
    Log_in_screen()

def User_check(username: str, password: str):
    """Provjerava postoji li upisana kombinacija korisničkog imena i lozinke u bazi podataka
        Ako postoji, otvara se glavni dio aplikacije. Ukoliko ne postoji prikazuje se pogreška

    Args:
        username (str): korisničko ime
        password (str): lozinka

    """
    result = log_in(username, password)

    if result:
        id = ID_current("Users.db", username, password)
        Create_user_table(username, id)
        Main_app(username, password)    
    else:
        text = "Krivo korisničko ime ili lozinka"
        Errot_Screen(text)

def Sign_in_screen():

    """
    Upisuje korisnika u bazu podataka
    """
    Sign_in_screen = tk.Tk()
    Sign_in_screen.title("Registracija korisnika")

    main_label = tk.LabelFrame(Sign_in_screen, text="Registriraj novog korisnika", labelanchor="nw")
    main_label.pack(expand=True, anchor=tk.CENTER)

    username_lable = tk.Label(main_label,text="Korisničko ime: ")
    password_lable = tk.Label(main_label, text="Lozinka: ")
    repeat_password_lable = tk.Label(main_label,text="Ponovite lozinku: ")

    username_entry = tk.Entry(main_label)
    password_entry = tk.Entry(main_label, show="*")
    repeat_password_entry = tk.Entry(main_label, show="*")

    username_lable.grid(pady = 5,padx= 5, column=0, row=0,sticky="ew")
    password_lable.grid(pady = 5,padx= 5, column=0, row=1,sticky="ew")
    repeat_password_lable.grid(pady = 5,padx= 5, column=0, row=2,sticky="ew")
    username_entry.grid(pady = 5,padx= 5, column=1, row=0,sticky="ew")
    password_entry.grid(pady = 5,padx= 5, column=1, row=1,sticky="ew")
    repeat_password_entry.grid(pady = 5,padx= 5, column=1, row=2,sticky="ew")

    secondary_label = tk.LabelFrame(Sign_in_screen)
    secondary_label.pack(expand=True, anchor=tk.N)
    save_data = tk.Button(secondary_label,text="Spremi", command= lambda:(sign_in(username_entry.get(), password_entry.get(),repeat_password_entry.get()), Sign_in_screen.destroy(), First_screen()))
    save_data.grid(row = 0, column = 0,sticky = "ew")
    return_to_main = tk.Button(secondary_label,text="Odustani", command= lambda:( Sign_in_screen.destroy(), First_screen()))
    return_to_main.grid(row = 0, column = 2, sticky = "ew")

def Log_in_screen():
    """
    Prijavljuje korisnika u aplikaciju 
    """

    log_in_screen = tk.Tk()
    log_in_screen.title("Registracija korisnika")

    main_label = tk.LabelFrame(log_in_screen, text="Prijavi se", labelanchor="nw")
    main_label.pack(expand=True, anchor=tk.CENTER)

    username_lable = tk.Label(main_label,text="Korisničko ime: ")
    password_lable = tk.Label(main_label, text="Lozinka: ")
    username_entry = tk.Entry(main_label)
    password_entry = tk.Entry(main_label, show="*")

    username_entry.grid(pady = 5,padx= 5, column=1, row=0,sticky="ew")
    password_entry.grid(pady = 5,padx= 5, column=1, row=1,sticky="ew")
    username_lable.grid(pady = 5,padx= 5, column=0, row=0,sticky="ew")
    password_lable.grid(pady = 5,padx= 5, column=0, row=1,sticky="ew")

    secondary_label = tk.LabelFrame(log_in_screen)
    secondary_label.pack(expand=True, anchor=tk.N)

    save_data = tk.Button(secondary_label,text="Prijavi se", command= lambda:(User_check(username = username_entry.get(), password = password_entry.get()), log_in_screen.destroy()))
    save_data.grid(row = 0, column = 0,sticky = "ew")
    return_to_main = tk.Button(secondary_label,text="Odustani", command= lambda: (log_in_screen.destroy(), First_screen()))
    return_to_main.grid(row = 0, column = 2, sticky = "ew")

def Edit_data_screen(username: str,password: str):
    """Otvara prozor za uređivanje korisničkih podataka

    Args:
        username (str): Korisničko ime
        password (str): Lozinka
    """
    edit_Data_screen = tk.Tk()
    edit_Data_screen.title("Uredi podatke")

    Frame = tk.LabelFrame(edit_Data_screen)
    Frame.pack()

    Username_label = tk.Label(Frame, text="Korisničko ime: ")
    Password_label = tk.Label(Frame, text="Lozinka: ")
    Username_entry = tk.Entry(Frame)
    Password_entry = tk.Entry(Frame, show="*")

    Username_label.grid(row=0, column=0)
    Username_entry.insert(tk.END, username)
    Password_label.grid(row=1, column=0)
    Password_entry.insert(tk.END, password)
    Username_entry.grid(row=0, column=1)
    Password_entry.grid(row=1, column=1)
    

    id = ID_current("Current_User.db", username, password)
    Update_entry(Username_entry, Password_entry, id)

    check = tk.Checkbutton(Frame, command = lambda: Show_password(Password_entry))
    check.grid(row=1, column=2)
    Save_data = tk.Button(Frame, text="Spremi", command= lambda:(change_data(id,Username_entry.get(), Password_entry.get())))

    Cancel_data = tk.Button(Frame, text="Odustani", command=lambda: edit_Data_screen.destroy())
    
    Save_data.grid(row=2, column=0, padx=5, pady=5)
    Cancel_data.grid(row=2, column=2, padx=5, pady=5)

First_screen()

