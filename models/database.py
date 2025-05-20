
import mysql.connector
from mysql.connector import errorcode

# Credentials
HOST = "localhost"
USER = "root"
PASSWORD = "admin"
DATABASE = "banking_db"

# Initial connection (no database selected)
initial_db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD
)
initial_cursor = initial_db.cursor()

# Create database if it doesn't exist
def create_database():
    try:
        initial_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        print(f"Database `{DATABASE}` ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

create_database()
initial_cursor.close()
initial_db.close()

# Now connect to the actual database
db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

cursor = db.cursor()

# Create tables only if they don't exist
TABLES = {}

TABLES['users'] = (
    "CREATE TABLE IF NOT EXISTS users ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  name VARCHAR(100),"
    "  email VARCHAR(100),"
    "  balance FLOAT"
    ") ENGINE=InnoDB"
)

TABLES['transactions'] = (
    "CREATE TABLE IF NOT EXISTS transactions ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  user_id INT,"
    "  amount FLOAT,"
    "  type ENUM('credit', 'debit'),"
    "  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

for table_name, table_sql in TABLES.items():
    try:
        print(f"Ensuring table `{table_name}` exists...")
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        print(f"Error creating table {table_name}: {err}")
