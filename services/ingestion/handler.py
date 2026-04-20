import json
from services.ingestion.parser_engine import parse_message
from services.ingestion.validators import validate_payload

def handler(event, context):
    body = event.get("body", "")
    if isinstance(body, str):
        body = json.loads(body)
    
    if not validate_payload(body):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid payload"})}
    
    extracted_data = parse_message(body.get("message", ""))
    
    # Placeholder: logic to save to database (pending)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Transaction ingestion successful",
            "data": extracted_data
        })
    }
