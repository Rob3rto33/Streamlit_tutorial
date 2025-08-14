import sqlite3
                                                #Used Sqlite so its done locally, and not have to set up a server with mysql


def init_db():                                             #basic table initialization and creation for users database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            birthday TEXT,
            fav_color TEXT,
            gender TEXT
        )
    ''')
       
    c.execute('''
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        date_of_application TEXT,
        leave_type TEXT,
        manager_name TEXT,
        comment TEXT,
        status TEXT DEFAULT 'Waiting'
    )
''')
    conn.commit()                                       #saving changes and closing connection
    conn.close()


                                                                #function to add a new user to the database
def add_user(role, first_name, last_name, email, password, birthday, fav_color, gender):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (role, first_name, last_name, email, password, birthday, fav_color, gender)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (role, first_name, last_name, email, password, birthday, fav_color, gender))
    conn.commit()
    conn.close()
                                            #close connection