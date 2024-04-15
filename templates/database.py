import sqlite3

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('database.db')

# Function to create the database schema
def create_schema():
    conn = connect_db()
    cursor = conn.cursor()

    with open('schema.sql') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

# Function to insert data into the names table
def insert_data(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO names (name) VALUES (?)", (name,))
    
    conn.commit()
    conn.close()
