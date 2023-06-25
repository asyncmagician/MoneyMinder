from db.models import Transaction, Balance
from sqlalchemy.orm import sessionmaker
from sqlalchemy import extract, desc, func, text, select
from datetime import datetime, timedelta

def get_all_transactions(db_connection):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    transactions = session.query(Transaction).all()

    session.close()

    return transactions

def check_balance_exists(db_engine):
    connection = db_engine.connect()
    result = connection.execute(select(func.count()).select_from(Balance))
    row_count = result.scalar()
    connection.close()
    return row_count > 0


def get_expenses_for_month(session, month, year):
    expenses = session.query(Transaction).filter(
        extract('month', Transaction.transaction_date) == month,
        extract('year', Transaction.transaction_date) == year,
        Transaction.type == "D"
    ).all()

    return expenses


def get_history_balance_updates(session, month, year):
    history_balance_updates = session.query(Balance).filter(
        extract('month', Balance.updated_at) == month,
        extract('year', Balance.updated_at) == year
    ).order_by(desc(Balance.updated_at)).all()

    return history_balance_updates

def get_current_month_transactions(db_engine):
    today = datetime.today()
    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        end_date = today.replace(year=today.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        end_date = today.replace(month=today.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

    with db_engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM transactions WHERE transaction_date >= :start_date AND transaction_date < :end_date AND (is_debited = 0 OR is_credited = 0)"),
                                    {"start_date": start_date, "end_date": end_date})
        return result.fetchall()

def update_transaction_status(db_engine, transaction_id, transaction_type):
    with db_engine.connect() as connection:
        transaction = connection.execute(text("SELECT * FROM transactions WHERE id = :transaction_id"),
                                         {"transaction_id": transaction_id}).first()
        if transaction_type == "D":
            new_status = not transaction.is_debited  
            connection.execute(text("UPDATE transactions SET is_debited = :new_status WHERE id = :transaction_id"), 
                               {"transaction_id": transaction_id, "new_status": new_status})
            if new_status:
                connection.execute(text("UPDATE balance SET account_balance = account_balance - :amount WHERE month = :month"), 
                                   {"amount": transaction.amount, "month": datetime.now().month})
            else:
                connection.execute(text("UPDATE balance SET account_balance = account_balance + :amount WHERE month = :month"), 
                                   {"amount": transaction.amount, "month": datetime.now().month})
        else:
            new_status = not transaction.is_credited  
            connection.execute(text("UPDATE transactions SET is_credited = :new_status WHERE id = :transaction_id"), 
                               {"transaction_id": transaction_id, "new_status": new_status})
            if new_status:
                connection.execute(text("UPDATE balance SET account_balance = account_balance + :amount WHERE month = :month"), 
                                   {"amount": transaction.amount, "month": datetime.now().month})
            else:
                connection.execute(text("UPDATE balance SET account_balance = account_balance - :amount WHERE month = :month"), 
                                   {"amount": transaction.amount, "month": datetime.now().month})
        
        connection.commit()

def get_most_recent_balance_update(db_connection):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    current_month = extract('month', func.now()) 

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