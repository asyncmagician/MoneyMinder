from dotenv import load_dotenv
from db.connection import create_db_engine
from db.queries import create_transaction, get_most_recent_balance_update, create_balance, get_current_month_transactions, update_transaction_status, get_history_balance_updates, get_expenses_for_month, check_balance_exists, delete_all_data, get_goals, calculate_forecast, save_goals, create_income, add_fixed_expenses
from db.models import Base
from datetime import datetime
from utils.helpers import validate_input
from utils.title import print_money_minder
from colorama import Fore, Style
from sqlalchemy.orm import sessionmaker
import os
import git
import calendar
import emoji

# Load environment variables from .env file
load_dotenv()  

# Get database credentials from environment variables
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')

# Create database engine and tables
db_engine = create_db_engine(host, user, password, database)
Base.metadata.create_all(db_engine)
Session = sessionmaker(bind=db_engine)

# Get the latest version tag from the git repository
repo = git.Repo(search_parent_directories=True)
tags = repo.tags

if tags and len(tags) >= 2:
    latest_tag = tags[1]
    version = latest_tag.name
else:
    version = "Unknown"

# Get the current year
current_year = datetime.now().year

# Check if balance exists in the database otherwise we won't let the user access the GUI yet
if not check_balance_exists(db_engine):
    try:
        print("\n" + "#" * 50)
        print(f"{Fore.CYAN}Welcome to MoneyMinder!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Version: {version} | ©BARTOLOMUCCI Antony ({current_year}){Style.RESET_ALL}")
        print("#" * 50 + "\n")  
        initial_balance = float(input("In order to start, please provide the current account balance: "))

        # Create the initial balance entry in the database
        balance_data = {
            "account_balance": initial_balance,
            "updated_at": datetime.now()
        }
        create_balance(db_engine, balance_data)
    # If the user is exiting with CTRL+C we intercept this interruption
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nProgram interrupted by user. Exiting...")
        db_engine.dispose()
        exit(0)
else:
    print("\n" + "#" * 50)
    print(f"{Fore.CYAN}Welcome back to MoneyMinder!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Version: {version} | ©BARTOLOMUCCI Antony ({current_year}){Style.RESET_ALL}")
    print("#" * 50 + "\n")  

dev_mode = False


try:
    while True:
        print("\n" + "-" * 50)
        print("\nWhat do you want to do?")
        print("")
        
        if dev_mode:
            print("[disable_dev] Disable developer mode")
            print("[delete_all] Delete all data")
        else:
            # Main menu options for regular mode
            print("[1] Check my balance")
            print("[2] Add an expense")
            print("[3] Add a refund")
            print("[4] Update status")
            print("[5] View balance history for a specific month")
            print("[6] View current month's expenses")
            print("[7] View expenses for a specific month")
            print("[8] Update balance")
            print("[9] See goals")
            print("[10] Add income")
            print("[11] View forecast")
            print("[12] Add fixed expenses")
            print(f"{Fore.RED}[devmode] Enable Developer Mode{Style.RESET_ALL}")
        
        print("[0] Quit")
        print("-" * 50 + "\n")       

        choice = input("Please, select a number:  ")


        if choice == "devmode":
            dev_mode = True
            print(f"{Fore.MAGENTA}Developer mode enabled. \nWith great powers, comes great responsibility, use it with cautious. {Style.RESET_ALL}")
            continue

        if not dev_mode:
            if choice == "1":
                most_recent_balance_update = get_most_recent_balance_update(db_engine)
                if most_recent_balance_update:
                    formatted_date = most_recent_balance_update.updated_at.strftime("%d/%m/%Y at %I:%M%p")
                    balance = most_recent_balance_update.account_balance

                    color = Style.RESET_ALL

                    if balance < 0:
                        color = Fore.RED
                    elif 0 <= balance <= 500:
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
                    "category": input("In which category is it for? (e.g. rent, food, gas...)  "),
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
                    "category": input("In which category is it for? (e.g. rent, food, gas...)  "),
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
                    eligible_transactions = [t for t in transactions if t.is_credited == 0 and t.is_debited == 0]
                    if eligible_transactions:
                        for transaction in eligible_transactions:
                            type_str = "None"
                            if transaction.type == "D":
                                type_str = "This is an expense"
                            elif transaction.type == "R":
                                type_str = "This is a refund"
                            print()
                            print(f"The identifier is {Fore.YELLOW}{transaction.id}{Style.RESET_ALL} \nThe description is '{transaction.description}' \nThe amount is {Fore.YELLOW}{transaction.amount}€{Style.RESET_ALL} \n{type_str}")
                            print()
                        transaction_id = int(input("Please, enter the ID of the transaction you want to update: "))
                        transaction_to_update = next((t for t in eligible_transactions if t.id == transaction_id), None)
                        if transaction_to_update:
                            update_transaction_status(db_engine, transaction_id, transaction_to_update.type)
                            print()
                            print(f"{Fore.GREEN}➪ The transaction status has been successfully updated.{Style.RESET_ALL}")
                        else:
                            print()
                            print(f"{Fore.RED}➪ Invalid transaction ID. Please try again.{Style.RESET_ALL}")
                    else:
                        print()
                        print(f"{Fore.RED}➪ No eligible transactions found for the current month.{Style.RESET_ALL}")
                else:
                    print()
                    print(f"{Fore.RED}➪ No transactions found for the current month.{Style.RESET_ALL}")
            elif choice == "5":
                        month = int(input("Which month? (1-12) "))
                        year = int(input("Which year? (1990-2099) "))

                        session = Session() 

                        history_balance_updates = get_history_balance_updates(session, month, year)

                        session.close()

                        if history_balance_updates:
                            print(f"\nBalance history for {month}/{year}:")
                            for balance_update in history_balance_updates:
                                formatted_date = balance_update.updated_at.strftime("%d/%m/%Y at %I:%M%p")
                                balance = balance_update.account_balance

                                color = Style.RESET_ALL

                                if balance < 0:
                                    color = Fore.RED
                                elif 0 <= balance <= 500:
                                    color = Fore.YELLOW
                                elif balance > 500:
                                    color = Fore.GREEN

                                print(f"- {formatted_date}: {color}{balance}€{Style.RESET_ALL}")
                        else:
                            print(f"\n{Fore.RED}No balance history found for {month}/{year}.{Style.RESET_ALL}")
            elif choice == "6":
                transactions = get_current_month_transactions(db_engine)
                if transactions:
                    total_amount = 0
                    credited_amount = 0
                    for transaction in transactions:
                        if transaction.type == "D":
                            total_amount += transaction.amount
                            if transaction.is_debited:
                                credited_amount += transaction.amount
                    
                    not_credited_amount = total_amount - credited_amount
                    
                    print(f"\nThis month, you have spent {Fore.BLUE}{total_amount}€{Style.RESET_ALL}.")
                    if credited_amount > 0:
                        print(f"{Fore.YELLOW}{credited_amount}€{Style.RESET_ALL} have been credited\nYou should be credited of {Fore.RED}{not_credited_amount}€{Style.RESET_ALL} soon.")
                    else:
                        print(f"No amount has been credited yet.")
                else:
                    print(f"\n{Fore.RED}No transactions found for the current month.{Style.RESET_ALL}")
            elif choice == "7":
                month = int(input("Which month? (1-12) "))
                year = int(input("Which year? (1990-2099) "))

                session = Session()

                expenses = get_expenses_for_month(session, month, year)

                session.close()

                if expenses:
                    print(f"\nExpenses for {month}/{year}:")
                    for expense in expenses:
                        formatted_date = expense.transaction_date.strftime("%d/%m/%Y at %I:%M%p")
                        amount = expense.amount
                        description = expense.description

                        print(f"- {formatted_date}: {description} {Fore.BLUE}({amount}€){Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}No expenses found for {month}/{year}.{Style.RESET_ALL}")
            elif choice == "8":
                most_recent_balance_update = get_most_recent_balance_update(db_engine)
                print(f"{Fore.RED}WARNING. You are going to manually change your balance, we do not recommand this way as it may be not accurate.{Style.RESET_ALL}")
                print(f"The current balance of the account is {most_recent_balance_update.account_balance}€")
                print()
                transaction_data = {
                    "account_balance": float(input("What is your new balance? ")),
                }
                create_balance(db_engine, transaction_data)
                print(f"{Fore.GREEN}➪ The balance has been successfully updated.{Style.RESET_ALL}")
            elif choice == "9":
                existing_goals = get_goals(db_engine)
                goals_exist = bool(existing_goals)

                if goals_exist:
                    print(f"{Fore.BLUE}This is your goals for the current month {Style.RESET_ALL}")
                    for month, goal in existing_goals.items():
                        month_name = calendar.month_name[month]
                        print(f"{emoji.emojize(':calendar: Month:')} {month_name}")
                        print(f"  {emoji.emojize(':house: Needs:')} {goal['needs']}€")
                        print(f"  {emoji.emojize(':red_heart:  Wants:')} {goal['wants']}€")
                        print(f"  {emoji.emojize(':money_bag: Saves:')} {goal['saves']}€")

                    print()

                    update_choice = input(f"{Fore.YELLOW}Goals for the current month already exist. Do you want to update them? (y/N){Style.RESET_ALL} ")
                    if update_choice.lower() == 'y':
                        salary = float(input("What is your monthly salary? "))
                        goals = {}
                        percentage_needs = float(input("Enter the percentage goal for needs: "))
                        percentage_wants = float(input("Enter the percentage goal for wants: "))
                        percentage_saves = float(input("Enter the percentage goal for saves: "))

                        needs = salary * (percentage_needs / 100)
                        wants = salary * (percentage_wants / 100)
                        saves = salary * (percentage_saves / 100)

                        goals['default'] = {
                            'needs': needs,
                            'wants': wants,
                            'saves': saves
                        }

                        save_goals(db_engine, goals)

                        print(f"{Fore.GREEN}Goals have been updated successfully.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Goals have not been updated.{Style.RESET_ALL}")

                else:
                    print(f"{Fore.RED}No goals have been detected in the database.{Style.RESET_ALL}")
                    create_new_goals = input("Do you want to create new goals for the current month? (y/N) ")
                    if create_new_goals.lower() == 'y':
                        salary = float(input("What is your monthly salary? "))
                        goals = {}
                        percentage_needs = float(input("In percentage, what's your main goal for all your needs? (e.g. rent, insurances..) "))
                        percentage_wants = float(input("In percentage, what's your main goal for all your wants? (e.g. restaurant, theater..) "))
                        percentage_saves = float(input("In percentage, what's your main goal for all the money you want to save? "))

                        needs = salary * (percentage_needs / 100)
                        wants = salary * (percentage_wants / 100)
                        saves = salary * (percentage_saves / 100)

                        goals['default'] = {
                            'needs': needs,
                            'wants': wants,
                            'saves': saves
                        }

                        save_goals(db_engine, goals)

                        print(f"{Fore.GREEN}New goals have been created successfully.{Style.RESET_ALL}")

                    else:
                        print(f"{Fore.YELLOW}No goals have been created.{Style.RESET_ALL}")

                print()
            elif choice == "10":
                income_amount = float(input("Enter your monthly income amount: "))
                create_income(db_engine, income_amount)
                print(f"{Fore.GREEN}➪ Your income has been successfully added.{Style.RESET_ALL}")
            elif choice == "11":
                forecast = calculate_forecast(db_engine)

                print(f"\nForecast:")
                print(f"Income: {forecast['income']}€")
                print(f"Total fixed expenses: {forecast['total_fixed_expenses']}€")
                print(f"Forecast balance: {forecast['forecast_balance']}€")
            elif choice == "12":
                result = add_fixed_expenses(db_engine)
                if result is None:
                    print(f"{Fore.RED}No income found for the current month. Please add an income first.{Style.RESET_ALL}")
                elif result:
                    print(f"{Fore.GREEN}➪ Fixed expenses have been added successfully.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}➪ Error occurred while adding fixed expenses.{Style.RESET_ALL}")
            elif choice == "0":
                db_engine.dispose()
                break
            else:
                print(f"{Fore.RED}➪ Invalid choices. Please try again.{Style.RESET_ALL}")
        else:
            if choice == "delete_all":
                confirm = input(f"{Fore.RED}Are you sure you want to delete all data? This action cannot be undone. (y/N){Style.RESET_ALL} ")
                if confirm.lower() == "y":
                    delete_all_data(db_engine)
                    print(f"{Fore.RED}All data has been deleted. \nPlease run the application, again.{Style.RESET_ALL}")
                    db_engine.dispose()
                    break
            elif choice == "disable_dev":
                dev_mode = False
            elif choice == "0":
                db_engine.dispose()
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
# If the user is exiting with CTRL+C we intercept this interruption
except KeyboardInterrupt:
    print(f"{Fore.RED}\nProgram interrupted by user. Exiting...")
finally:
    print(f"{Fore.MAGENTA}\nThanks for choosing MoneyMinder")
    db_engine.dispose()