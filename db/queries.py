from db.models import Transaction, Solde
from sqlalchemy.orm import sessionmaker
from datetime import datetime

def get_all_transactions(db_connection):
    Session = sessionmaker(bind=db_connection)
    session = Session()

    transactions = session.query(Transaction).all()

    session.close()

    return transactions
