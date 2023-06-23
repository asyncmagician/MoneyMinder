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
    is_debited = Column(Boolean)
    is_credited = Column(Boolean)

class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True)
    account_balance = Column(Float)
    updated_at = Column(DateTime)
