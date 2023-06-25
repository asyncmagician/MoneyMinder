from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_date = Column(DateTime)
    description = Column(String(255))
    amount = Column(Float)
    type = Column(String(50))
    category = Column(String(255))
    is_debited = Column(Boolean)
    is_credited = Column(Boolean)

class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True)
    account_balance = Column(Float)
    month = Column(Integer)
    updated_at = Column(DateTime)

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    month = Column(Integer)
    year = Column(Integer)
    needs = Column(Integer)
    wants = Column(Integer)
    saves = Column(Integer)
    updated_at = Column(DateTime)