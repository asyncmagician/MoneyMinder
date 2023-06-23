from datetime import datetime

def format_amount(amount):
    return f"${amount:.2f}" 

def get_current_month():
    now = datetime.now()
    return now.month, now.year

def validate_input(transaction_data):
    required_fields = ["transaction_date", "description", "amount", "type"]
    for field in required_fields:
        if field not in transaction_data or not transaction_data[field]:
            print(f"ERROR: Invalid field: {field}")
            return False
    return True

