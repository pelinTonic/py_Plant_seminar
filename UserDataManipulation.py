from dbmanager.db_manager import *


def sign_in(username: str, password: str, repeat_password: str):
    """
    Upisuje korisnika u bazu podataka

    Args:
        username: str
        password: str
        repeat_password: str
    """
    if repeat_password == password:
        db_file = "Users.db"
    
        create_table_sql = """

        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL,
            RepeatPassword TEXT NOT NULL
        );
        """
        insert_into_table_sql = """
        INSERT INTO Users (Username, Password, RepeatPassword)
        VALUES (?, ?, ?);
        """
        sql_connection = create_connection(db_file)
        success = create_table(sql_connection, create_table_sql)
        if success:
            print("Uspjesno smo napravili tablicu")
        else:
            print("Nismo napravili tablicu")

        data = [(username, password, repeat_password)]
        
        success = insert_into_table(sql_connection, insert_into_table_sql, data)
        if success:
            print("Uspjesno smo dodali podatke u tablicu")
        else:
            print("Nismo dodali podatke u tablicu")


        sql_connection.close()
    else:
        print("Lozinka i ponovljena lozinka moraju bit iste")

def ID_current(db_file: str, username: str, password: str) -> bool:

    """Dohvaća ID trenutno prijavljenog korisnika ii baze podataka
        Args:
            db_file: str
            username: str
            password: str
        """

    db_file = db_file
  
    if db_file == "Users.db":
        search_sql = """
        SELECT id from Users WHERE username = ? AND password = ?
        """
        sql_connection =create_connection(db_file)
        data = [(username, password)]

        search = get_ID(sql_connection, search_sql, data)
        search = search[0]

        return search

    else:
        
        search_sql = """
        SELECT database_ID from Current_User WHERE username = ?
        """
        sql_connection =create_connection(db_file)
        data = [(username,)]
    

        search = get_ID(sql_connection, search_sql, data)
        search = search[0]

        return search

def log_in(username: str, password: str)-> bool:
    """
    Provjerava je li korisnik u bazi podataka
    Args: 
        seurname: str
        password: str
    """
    db_file = "Users.db"

    search_sql = """
    SELECT * from Users WHERE username = ? AND password = ?
    """

    sql_connection =create_connection(db_file)
    data = [(username, password)]

    search = check_if_value_exists(sql_connection, search_sql, data)

    if search:
        return True
    else:
        return False
        
def change_data(id: str, username: str, password: str):
    """
    Promjena korisničkih podataka u bazi podataka
    id: str
    username: str
    password: str 
    """

    db_file = "Users.db"


    sql_connection =create_connection(db_file)
    update_sql = """
        UPDATE users SET username = ?, password = ? WHERE id = ?
        """
    data = (username, password, id)
    update_entry(sql_connection, update_sql, data)
        
def return_username(database_ID):
    """
    Provjerava je li korisnik u bazi podataka
    """
    db_file = "Users.db"

    search_sql = """

    SELECT username from Users WHERE id = ?
    """

    sql_connection =create_connection(db_file)
    data = [(database_ID,)]

    search = get_data(sql_connection, search_sql, data)

    if search:
        return search
    else:
        return False

def return_password(database_ID):

    db_file = "Users.db"

    search_sql = """

    SELECT password from Users WHERE id = ?
    """

    sql_connection =create_connection(db_file)
    data = [(database_ID,)]

    search = get_data(sql_connection, search_sql, data)

    if search:
        return search
    else:
        return False

def delete_current_user():

    db_file = "Current_User.db"

    delete_sql = """
    DROP TABLE IF EXISTS Current_User
    """

    sql_connection =create_connection(db_file)

    delete_entry(sql_connection, delete_sql)
