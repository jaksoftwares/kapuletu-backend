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
    Primary entry point for the Twilio Webhook (AWS Lambda Handler).
    
    This function:
    1. Receives raw traffic from API Gateway (Twilio webhook).
    2. Normalizes the payload (handles Base64, JSON vs Form-Encoded).
    3. Initializes the database session and business logic service.
    4. Routes the payload to the IngestionService for parsing and storage.
    
    Args:
        event (dict): AWS Lambda event containing the HTTP request data.
        context (object): AWS Lambda context.
        
    Returns:
        dict: API Gateway compatible response (statusCode, body).
    """
    logger.info("Received Ingestion Webhook request")
    
    # 1. Payload Extraction & Normalization
    # Twilio typically sends data as 'application/x-www-form-urlencoded'.
    # If using a proxy or direct API call, it might be Base64 encoded.
    body = event.get("body", "")
    is_base64 = event.get("isBase64Encoded", False)
    
    if is_base64:
        import base64
        try:
            body = base64.b64decode(body).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to decode base64 body: {e}")
            return {"statusCode": 400, "body": json.dumps({"error": "invalid_encoding"})}
        
    # Determine the content type to parse correctly (Form-Encoded vs JSON)
    headers = {k.lower(): v for k, v in event.get("headers", {}).items()}
    content_type = headers.get("content-type", "")

    if "application/json" in content_type:
        payload = json.loads(body)
    else:
        # Standard Twilio payload parsing
        payload = {k: v[0] for k, v in parse_qs(body).items()}

    # Guard clause: Every Twilio message must have a Body
    if not payload.get("Body"):
        logger.warning("Rejected request: Missing message Body")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing message body"})
        }

    # 2. Database Session Initialization
    # SessionLocal is the SQLAlchemy session generator from common/database.py
    db = SessionLocal()
    
    try:
        # 3. Invoke Ingestion Service Logic
        # The service layer handles the core business logic (parsing, owner resolution, idempotency)
        ingestion_service = IngestionService(db)
        result = ingestion_service.process_webhook(payload)
        
        # Determine HTTP status based on business outcome
        status_code = 201
        if result["status"] == "ignored":
            # 200 OK for duplicates (prevents Twilio from retrying unnecessarily)
            status_code = 200
        elif result["status"] == "error":
            # 401 if the phone number doesn't map to a registered treasurer
            status_code = 401 

        return {
            "statusCode": status_code,
            "body": json.dumps(result)
        }
        
    except Exception as e:
        # Global error catch-all to prevent raw leakage and ensure logging
        logger.error(f"CRITICAL: Unexpected error in ingestion handler: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "internal_server_error", "message": str(e)})
        }
    finally:
        # ALWAYS close the database session to prevent connection leaks
        db.close()
