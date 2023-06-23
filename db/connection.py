from sqlalchemy import create_engine
from mysql.connector import Error

def create_db_engine(host, user, password, db):
    engine = None
    try:
        engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db}", echo=True)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return engine
