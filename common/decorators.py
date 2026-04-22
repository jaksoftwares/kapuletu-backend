import json
import functools
from common.auth import decode_access_token
from common.database import SessionLocal
from models.subscription import Subscription, Plan

def with_auth(role_required=None):
    def decorator(handler):
        @functools.wraps(handler)
        def wrapper(event, context):
            auth_header = event.get("headers", {}).get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return {"statusCode": 401, "body": json.dumps({"error": "Missing token"})}
            
            token = auth_header.split(" ")[1]
            payload = decode_access_token(token)
            
            if not payload:
                return {"statusCode": 401, "body": json.dumps({"error": "Invalid token"})}
            
            # RBAC check
            if role_required and payload.get("role") != role_required:
                return {"statusCode": 403, "body": json.dumps({"error": "Insufficient permissions"})}
            
            # Inject user info into event
            event["user_id"] = payload.get("sub")
            event["role"] = payload.get("role")
            
            return handler(event, context)
        return wrapper
    return decorator

def with_subscription_check(required_feature=None):
    def decorator(handler):
        @functools.wraps(handler)
        def wrapper(event, context):
            user_id = event.get("user_id")
            if not user_id:
                 return {"statusCode": 401, "body": json.dumps({"error": "User context missing"})}
            
            db = SessionLocal()
            subscription = db.query(Subscription).filter(Subscription.user_id == user_id, Subscription.status == "active").first()
            
            if not subscription:
                return {"statusCode": 402, "body": json.dumps({"error": "Active subscription required"})}
            
            # Logic to check plan limits could go here
            
            db.close()
            return handler(event, context)
        return wrapper
    return decorator
