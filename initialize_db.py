import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
}

def create_database():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS pharmacy_db")
            cursor.execute("USE pharmacy_db")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pharmacy_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """)
            connection.commit()
            print("Database and table created successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    create_database()
