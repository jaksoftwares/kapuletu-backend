import re

def parse_message(message_text):
    # Basic RegEx for common MPESA-like message formats
    # Example: "Confirmed. KES 500.00 from 254712345678 to KAPULETU"
    
    amount_match = re.search(r"KES ([\d,.]+)", message_text)
    phone_match = re.search(r"from (\d+)", message_text)
    
    return {
        "amount": amount_match.group(1) if amount_match else None,
        "phone": phone_match.group(1) if phone_match else None,
        "raw": message_text
    }
