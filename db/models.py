from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True)
    month = Column(Integer)
    year = Column(Integer)
    amount = Column(Float)
    updated_at = Column(DateTime)

class FixedExpense(Base):
    __tablename__ = 'fixed_expenses'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    amount = Column(Float)
    income_id = Column(Integer, ForeignKey('income.id'))

    income = relationship("Income", backref="fixed_expenses")
