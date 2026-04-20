import datetime
import uuid

def format_currency(amount):
    return f"KES {amount:,.2f}"

def generate_id():
    return str(uuid.uuid4())
