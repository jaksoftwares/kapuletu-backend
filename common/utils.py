import datetime
import uuid

def format_currency(amount: float) -> str:
    """
    Converts a numeric amount into a standardized Kenyan Shillings currency string.
    
    Args:
        amount (float or int): The monetary value.
        
    Returns:
        str: Formatted string (e.g., "KES 1,250.00").
    """
    return f"KES {amount:,.2f}"

def generate_id() -> str:
    """
    Generates a unique identifier using UUID4.
    
    Returns:
        str: A version 4 Universally Unique Identifier string.
    """
    return str(uuid.uuid4())
