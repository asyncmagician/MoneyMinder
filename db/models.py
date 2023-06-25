from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_date = Column(DateTime)  # Date of the transaction
    description = Column(String(255))  # Description of the transaction
    amount = Column(Float)  # Amount of the transaction
    type = Column(String(50))  # Type of transaction (e.g., 'D' for debit, 'C' for credit)
    category = Column(String(255))  # Category of the transaction
    is_debited = Column(Boolean)  # Flag indicating if the transaction is debited
    is_credited = Column(Boolean)  # Flag indicating if the transaction is credited

class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True)
    account_balance = Column(Float)  # Account balance
    month = Column(Integer)  # Month of the balance update
    updated_at = Column(DateTime)  # Date and time of the balance update

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    month = Column(Integer)  # Month of the goal
    year = Column(Integer)  # Year of the goal
    needs = Column(Integer)  # Goal amount for needs
    wants = Column(Integer)  # Goal amount for wants
    saves = Column(Integer)  # Goal amount for savings
    updated_at = Column(DateTime)  # Date and time of the goal update

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True)
    month = Column(Integer)  # Month of the income
    year = Column(Integer)  # Year of the income
    amount = Column(Float)  # Income amount
    updated_at = Column(DateTime)  # Date and time of the income update

class FixedExpense(Base):
    __tablename__ = 'fixed_expenses'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))  # Description of the fixed expense
    amount = Column(Float)  # Amount of the fixed expense
    income_id = Column(Integer, ForeignKey('income.id'))  # Foreign key referencing the income table

    income = relationship("Income", backref="fixed_expenses")  # Relationship between FixedExpense and Income tables
