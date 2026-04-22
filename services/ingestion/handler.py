import json
import logging
from common.database import SessionLocal
from services.ingestion.service import IngestionService
from urllib.parse import parse_qs

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(event, context):
    """
    Twilio Webhook Handler
    """
    logger.info("Received Twilio Webhook")
    
    # 1. Extract Payload
    # Twilio sends data as form-encoded by default
    body = event.get("body", "")
    is_base64 = event.get("isBase64Encoded", False)
    
    if is_base64:
        import base64
        body = base64.b64decode(body).decode("utf-8")
        
    # Parse form data OR json
    if event.get("headers", {}).get("Content-Type") == "application/json":
        payload = json.loads(body)
    else:
        # standard twilio x-www-form-urlencoded
        payload = {k: v[0] for k, v in parse_qs(body).items()}

    if not payload.get("Body"):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing message body"})
        }

    # 2. Database Session
    db = SessionLocal()
    
    try:
        # 3. Invoke Service
        ingestion_service = IngestionService(db)
        result = ingestion_service.process_webhook(payload)
        
        status_code = 201
        if result["status"] == "ignored":
            status_code = 200
        elif result["status"] == "error":
            status_code = 401 # Unauthorized phone

        return {
            "statusCode": status_code,
            "body": json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Unexpected error in ingestion handler: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "internal_server_error"})
        }
    finally:
        db.close()
