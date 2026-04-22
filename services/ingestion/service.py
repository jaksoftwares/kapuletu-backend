import logging
import hashlib
from sqlalchemy.orm import Session
from services.ingestion.parser_engine import parse_message
from repositories.transaction_repo import TransactionRepository
from models.pending_transaction import PendingTransaction
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TransactionRepository(db)

    def process_webhook(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main business logic for ingestion.
        1. Resolve Treasurer (owner)
        2. Parse Message
        3. Enforce Idempotency
        4. Persist to Pending Queue
        """
        message_body = raw_payload.get("Body", "").strip()
        sender_phone = raw_payload.get("From", "")
        
        logger.info(f"Ingesting message from {sender_phone}: {message_body[:50]}...")

        # 1. Resolve Owner (Treasurer)
        owner = self.repo.resolve_owner_by_phone(sender_phone)
        if not owner:
            logger.warning(f"No treasurer found for phone: {sender_phone}")
            return {"status": "error", "message": "unauthorized_phone"}

        # 2. Parse Logic (AI + Regex Hybrid)
        parsed_data = parse_message(message_body)
        
        # 3. Idempotency Check
        # Primary: Transaction Code (e.g. QE771...)
        # Secondary: Hash of (Owner + Body) for manual entries without codes
        txn_code = parsed_data.get("transaction_code")
        if not txn_code:
            # Fallback idempotency key: Hash the context
            context_string = f"{owner.user_id}:{message_body}"
            txn_code = f"HASH-{hashlib.md5(context_string.encode()).hexdigest()[:12]}"
            parsed_data["transaction_code"] = txn_code

        if self.repo.check_duplicate_transaction_code(txn_code):
            logger.info(f"Duplicate entry detected (Code/Hash: {txn_code}). Ignoring.")
            return {"status": "ignored", "message": "duplicate_entry", "code": txn_code}

        # 4. Create Pending Record
        pending_txn = PendingTransaction(
            owner_id=owner.user_id,
            raw_message=message_body,
            sender_name=parsed_data.get("sender_name"),
            amount=parsed_data.get("amount"),
            currency=parsed_data.get("currency") or "KES",
            transaction_code=txn_code,
            sender_phone=parsed_data.get("phone") or sender_phone,
            purpose=parsed_data.get("purpose"),
            confidence_score=parsed_data.get("confidence_score"),
            workflow_status="pending"
        )
        
        saved_txn = self.repo.insert_pending_transaction(pending_txn)
        
        logger.info(f"Successfully processed transaction. ID: {saved_txn.pending_id}, Confidence: {saved_txn.confidence_score}")
        
        return {
            "status": "success",
            "pending_id": str(saved_txn.pending_id),
            "owner_id": str(owner.user_id),
            "parsed_data": parsed_data
        }
