import sqlite3
import os
DATABASE="database/students.db"

def get_connection():
    os.makedirs("database",exist_ok=True)

    connection=sqlite3.connect(DATABASE)
    connection.row_factory=sqlite3.Row
    return connection

def initialize_database():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS
    students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    course TEXT NOT NULL)
    """)
    connection.commit()
    connection.close()
