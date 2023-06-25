from db.models import Transaction, Balance, Goal
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import extract, desc, func, text, select, delete, insert, and_
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
        category=transaction_data.get('category', ""),
        is_debited=transaction_data.get('is_debited', False),
        is_credited=transaction_data.get('is_credited', False)
    )

    session.add(new_transaction)
    session.commit()
    session.close()

def create_balance(db_connection, balance_data):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    current_month = datetime.now().month

    new_balance = Balance(
        account_balance=balance_data.get('account_balance', 0),
        month=current_month,
        updated_at=balance_data.get('updated_at', datetime.now())
    )

    session.add(new_balance)
    session.commit()
    session.close()


def get_goals(db_engine):
    with db_engine.connect() as connection:
        result = connection.execute(select(Goal))
        goals = {}
        for row in result:
            goals[row.month] = {
                'needs': row.needs,
                'wants': row.wants,
                'saves': row.saves
            }
        return goals


from datetime import datetime

def save_goals(db_engine, goals):
    Session = sessionmaker(bind=db_engine)
    session = Session()

    current_year = datetime.now().year
    current_month = datetime.now().month
    
    existing_goals = session.query(Goal).filter(and_(Goal.month == current_month, Goal.year == current_year)).all()

    if existing_goals:
        for goal in existing_goals:
            goal.needs = goals['default']['needs']
            goal.wants = goals['default']['wants']
            goal.saves = goals['default']['saves']
            goal.updated_at = datetime.now()
    else:
        goal = Goal(
            month=current_month,
            year=current_year,
            updated_at=datetime.now(),
            needs=goals['default']['needs'],
            wants=goals['default']['wants'],
            saves=goals['default']['saves']
        )
        session.add(goal)

    session.commit()
    session.close()




def calculate_forecast(db_engine):
    goals = get_goals(db_engine)
    total_goal_amount = sum(goal['needs'] + goal['wants'] + goal['saves'] for goal in goals.values())

    transactions = get_current_month_transactions(db_engine)

    forecast = {}

    for category, goal_values in goals.items():
        category_transactions = [t for t in transactions if t.category == category]
        category_expenses = sum([t.amount for t in category_transactions if t.type == 'D'])

        forecast_amount = {
            'needs': goal_values['needs'] - category_expenses,
            'wants': goal_values['wants'] - category_expenses,
            'saves': goal_values['saves'] - category_expenses
        }

        forecast[category] = forecast_amount

    return forecast








# Developer Mode

def delete_all_data(db_engine):
    with db_engine.begin() as connection:
        delete_stmt = delete(Transaction)
        connection.execute(delete_stmt)

        delete_stmt = delete(Balance)
        connection.execute(delete_stmt)