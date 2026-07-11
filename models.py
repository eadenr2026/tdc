import sqlite3

DATABASE = "tdc.db"

# function to connect to database
def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection
# function to initialize database
def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL)""")
    connection.commit()
    connection.close()

# creates user accounts and stores hashed password to register in db
def create_user(username, password_hash):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO user_accounts (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    connection.commit()
    connection.close()

# finds user id, username, hashed_pass if username found in db
def find_user(username):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_accounts WHERE username = ?", (username,))

    user = cursor.fetchone()
    connection.close()

    return user