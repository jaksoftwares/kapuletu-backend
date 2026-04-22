import json
import uuid
from services.ingestion.parser_engine import parse_message
from services.ingestion.validators import validate_payload
from common.database import SessionLocal
from models.pending_transaction import PendingTransaction

def handler(event, context):
    """
    Ingestion Handler:
    Invoked by Twilio Webhook (via API Gateway)
    """
    body = event.get("body", "")
    if isinstance(body, str):
        body = json.loads(body)
    
    if not validate_payload(body):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid payload"})}
    
    message_text = body.get("message", "")
    extracted_data = parse_message(message_text)
    
    db = SessionLocal()
    try:
        # Create a pending transaction record
        # Note: In a production SaaS, we'd resolve the 'owner_id' 
        # by looking up the phone number in our 'Groups' or 'Users' table.
        
        pending = PendingTransaction(
            pending_id=uuid.uuid4(),
            raw_text=message_text,
            amount=extracted_data.get("amount"),
            sender_phone=extracted_data.get("phone"),
            transaction_code=extracted_data.get("code") or f"TMP-{uuid.uuid4().hex[:8]}",
            is_processed=False
        )
        
        db.add(pending)
        db.commit()
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Ingestion successful",
                "pending_id": str(pending.pending_id)
            })
        }
    except Exception as e:
        db.rollback()
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        db.close()
