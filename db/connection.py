import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name: str, user_name: str, user_password: str, db_name: str):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
