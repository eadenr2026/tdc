import sqlite3

DATABASE = "tdc.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL)""") # Create Table goes here
    connection.commit()
    connection.close()

def create_user(username, password_hash):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO user_accounts (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    connection.commit()
    connection.close()