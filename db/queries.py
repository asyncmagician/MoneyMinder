from db.models import Transaction, Balance
from sqlalchemy.orm import sessionmaker
from sqlalchemy import extract, desc, func
from datetime import datetime

def get_all_transactions(db_connection):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    transactions = session.query(Transaction).all()

    session.close()

    return transactions

def get_most_recent_balance_update(db_connection):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    current_month = extract('month', func.now())  # Get the current month

    most_recent_update = session.query(Balance).filter(
        Balance.month == current_month
    ).order_by(desc(Balance.updated_at)).first()

    session.close()

    return most_recent_update

def create_transaction(db_connection, transaction_data):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    new_transaction = Transaction(
        transaction_date=transaction_data.get('transaction_date', datetime.now()),
        description=transaction_data.get('description', ""),
        amount=transaction_data.get('amount', 0),
        type=transaction_data.get('type', ""),
        is_debited=transaction_data.get('is_debited', False),
        is_credited=transaction_data.get('is_credited', False)
    )

    session.add(new_transaction)
    session.commit()
    session.close()

def create_balance(db_connection, balance_data):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    current_month = extract('month', func.now())  

    new_balance = Balance(
        account_balance=balance_data.get('account_balance', 0),
        month=current_month, 
        updated_at=balance_data.get('updated_at', datetime.now())
    )

    session.add(new_balance)
    session.commit()
    session.close()