from dotenv import load_dotenv
from db.connection import create_db_engine
from db.queries import create_transaction, get_most_recent_balance_update, create_balance, get_current_month_transactions, update_transaction_status
from db.models import Base
from datetime import datetime
from utils.helpers import validate_input
from utils.title import print_money_minder
from colorama import Fore, Style
import os

load_dotenv()  


host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')

db_engine = create_db_engine(host, user, password, database)
Base.metadata.create_all(db_engine)

try:
    while True:
        print("\n" + "-" * 50)
        print("\nWhat do you want to do?")
        print("")
        print("[1] Check my balance")
        print("[2] Add an expense")
        print("[3] Add a refund")
        print("[4] Update status")
        print("[5] View balance history for a specific month")
        print("[6] View current month's expenses")
        print("[7] View expenses for a specific month")
        print("[8] Update balance")
        print("[0] Quit")
        print("-" * 50 + "\n")        


        choice = input("Please, select a number:  ")

        if choice == "1":
            most_recent_balance_update = get_most_recent_balance_update(db_engine)
            if most_recent_balance_update:
                formatted_date = most_recent_balance_update.updated_at.strftime("%d/%m/%Y at %I:%M%p")
                balance = most_recent_balance_update.account_balance

                color = Style.RESET_ALL

                if balance < 0:
                    color = Fore.RED
                elif 0 <= balance < 500:
                    color = Fore.YELLOW
                elif balance > 500:
                    color = Fore.GREEN

                print(f"➪ The most recent balance update was on {formatted_date} "
                    f"and the balance was {color}{balance}€{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}➪ No balance updates found for the current month.{Style.RESET_ALL}")
        elif choice == "2":
            transaction_data = {
                "transaction_date": datetime.now(),
                "description": input("What is the description?  "),
                "amount": float(input("What is the amount? ")),
                "type": "D",
                "is_debited": False,
                "is_credited": False,
            }

            if validate_input(transaction_data):
                create_transaction(db_engine, transaction_data)
                print(f"{Fore.GREEN}➪ The expense has been successfully added.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}➪ Invalid input. Please try again.{Style.RESET_ALL}")
            
        elif choice == "3":
            transaction_data = {
                "transaction_date": datetime.now(),
                "description": input("What is the description? "),
                "amount": float(input("What is the amount? ")),
                "type": "R",
                "is_debited": False,
                "is_credited": False
            }

            if validate_input(transaction_data):
                create_transaction(db_engine, transaction_data)
                print(f"{Fore.GREEN}➪ The refund has been successfully added.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}➪ Invalid input. Please try again.{Style.RESET_ALL}")
        elif choice == "4":
            transactions = get_current_month_transactions(db_engine)
            if transactions:
                for transaction in transactions:
                    type : str = "None"
                    if(transaction.type == "D"):
                        type: str = "This is an expense"
                    elif(transaction.type == "R"):
                        type: str = "This is a refund"
                    print()
                    print(f"The identifier is {Fore.YELLOW}{transaction.id}{Style.RESET_ALL} \nThe description is '{transaction.description}' \nThe amount is {Fore.YELLOW}{transaction.amount}€{Style.RESET_ALL} \n{type}")
                    print()
                transaction_id = int(input("Please, enter the ID of the transaction you want to update: "))
                for transaction in transactions:
                    if transaction.id == transaction_id:
                        transaction_type = transaction.type
                update_transaction_status(db_engine, transaction_id, transaction_type)
                print()
                print(f"{Fore.GREEN}➪ The transaction status has been successfully updated.{Style.RESET_ALL}")
            else:
                print()
                print(f"{Fore.RED}➪ No transactions found for the current month.{Style.RESET_ALL}")
        elif choice == "5":
            # View balance history for a specific month
            pass
        elif choice == "6":
            # View current month's expenses
            pass
        elif choice == "7":
            # View expenses for a specific month
            pass
        elif choice == "8":
            transaction_data = {
                "account_balance": float(input("Your balance : ")),
            }
            create_balance(db_engine, transaction_data)
            print("➪ The balance has been successfully updated.")
        elif choice == "0":
            db_engine.dispose()
            break
        else:
            print("➪ Invalid choices. Please try again.")
except KeyboardInterrupt:
    print(f"{Fore.RED}\nProgram interrupted by user. Exiting...")
finally:
    print(f"{Fore.MAGENTA}\nThanks for choosing MoneyMinder")
    db_engine.dispose()