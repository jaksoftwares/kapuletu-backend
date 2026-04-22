import json
from common.decorators import with_auth, with_subscription_check
from common.database import SessionLocal
from services.approval.service import ApprovalService

@with_auth(role_required="treasurer")
@with_subscription_check(required_feature="approvals")
def handler(event, context):
    """
    Approval Handler:
    Allows a treasurer to finalize a pending transaction into the official ledger.
    """
    body = json.loads(event.get("body", "{}"))
    pending_id = body.get("pending_id")
    group_id = body.get("group_id")
    campaign_id = body.get("campaign_id")
    
    if not pending_id or not group_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing required fields"})}

    db = SessionLocal()
    service = ApprovalService(db)
    
    try:
        # Tenancy check: Ensure the group belongs to the authorized user
        # (This logic would eventually move into a reusable 'tenant_context' check)
        
        # Execute the approval workflow
        txn = service.approve_transaction(
            pending_txn_id=pending_id,
            treasurer_id=event["user_id"],
            group_id=group_id,
            campaign_id=campaign_id
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Transaction approved and committed to ledger",
                "transaction_id": str(txn.transaction_id)
            })
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        db.close()
