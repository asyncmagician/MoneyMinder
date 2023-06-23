from datetime import datetime

def format_amount(amount):
    return f"${amount:.2f}" 

def get_current_month():
    now = datetime.now()
    return now.month, now.year
