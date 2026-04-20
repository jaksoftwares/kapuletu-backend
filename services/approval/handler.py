import json
from services.approval.service import approve_transaction, reject_transaction

def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    action = body.get("action")
    transaction_id = body.get("transaction_id")
    
    if action == "approve":
        result = approve_transaction(transaction_id)
    elif action == "reject":
        result = reject_transaction(transaction_id)
    else:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid action"})}
        
    return {"statusCode": 200, "body": json.dumps(result)}
