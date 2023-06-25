from sqlalchemy import create_engine
from mysql.connector import Error

def create_db_engine(host, user, password, db):
    engine = None
    try:
        engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db}")
        print()
        print("✅ \033[32mConnection to MySQL database has been successful\033[0m")
        print("")
    except Error as e:
        print("\033[91mThe error '{}' occurred\033[0m".format(e))
    return engine
