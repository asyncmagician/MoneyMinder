from dotenv import load_dotenv
from db.connection import create_db_engine
from db.queries import create_transaction
from db.models import Base
from datetime import datetime
from utils.helpers import validate_input
from utils.title import print_money_minder
import os

load_dotenv()  


host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')

db_engine = create_db_engine(host, user, password, database)
Base.metadata.create_all(db_engine)

while True:
    print("What do you want to do?")
    print("")
    print("[1] Check my balance")
    print("[2] Add an expense")
    print("[3] Add a refund")
    print("[4] Update status")
    print("[5] View current month's balance")
    print("[6] View balance history for a specific month")
    print("[7] View current month's expenses")
    print("[8] View expenses for a specific month")
    print("[0] Quit")


    choice = input("Please, select a number:  ")

    if choice == "1":
        # check balance logic
        pass
    elif choice == "2":
        transaction_data = {
            "transaction_date": datetime.now(),
            "description": input("Description : "),
            "amount": float(input("Montant : ")),
            "type": "D",
            "is_debited": False,
            "is_credited": False,
        }

        if validate_input(transaction_data):
            create_transaction(db_engine, transaction_data)
            print("The expense has been successfully added.")
        else:
            print("Invalid input. Please try again.")
        
    elif choice == "3":
        transaction_data = {
            "transaction_date": datetime.now(),
            "description": input("Description : "),
            "amount": float(input("Montant : ")),
            "type": "R",
            "is_debited": False,
            "is_credited": False
        }

        if validate_input(transaction_data):
            create_transaction(db_engine, transaction_data)
            print("The refund has been successfully added.")
        else:
            print("Invalid input. Please try again.")
    elif choice == "4":
        # update status logic
        pass
    elif choice == "5":
        # View current month's balance
        pass
    elif choice == "6":
        # View balance history for a specific month
        pass
    elif choice == "7":
        # View current month's expenses
        pass
    elif choice == "8":
        # View expenses for a specific month
        pass
    elif choice == "0":
        db_engine.dispose()
        break
    else:
        print("Invalid choices. Please try again.")

db_engine.dispose()