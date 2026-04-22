from sqlalchemy.orm import Session
from models.transaction import Transaction
from models.pending_transaction import PendingTransaction
from common.qldb import get_qldb_driver
from common.logger import get_logger

logger = get_logger(__name__)

class ApprovalService:
    def __init__(self, db: Session):
        self.db = db
        self.qldb = get_qldb_driver()

    def approve_transaction(self, pending_txn_id, treasurer_id, group_id, campaign_id=None):
        """
        Main workflow for approving a pending transaction.
        1. Fetch pending transaction
        2. Create final transaction record
        3. Write to QLDB immutable ledger
        4. Mark pending as processed
        """
        pending = self.db.query(PendingTransaction).filter(PendingTransaction.id == pending_txn_id).first()
        if not pending:
            raise Exception("Pending transaction not found")

        # 1. Create Transaction record
        new_txn = Transaction(
            owner_id=treasurer_id,
            group_id=group_id,
            campaign_id=campaign_id,
            transaction_code=pending.transaction_code,
            amount=pending.amount,
            sender_phone=pending.sender_phone,
            status="approved"
        )
        self.db.add(new_txn)
        self.db.flush() # Get the new_txn.transaction_id

        # 2. Write to QLDB (The immutable truth)
        try:
            self._write_to_ledger(new_txn)
        except Exception as e:
            logger.error(f"Failed to write to QLDB: {e}")
            self.db.rollback()
            raise Exception("Ledger commitment failed")

        # 3. Cleanup pending
        pending.is_processed = True
        
        self.db.commit()
        return new_txn

    def _write_to_ledger(self, txn: Transaction):
        # In a real implementation, this would use the QLDB driver to execute Ion-formatted insertion
        # qldb_txn.execute_statement("INSERT INTO LedgerTransactions ?", txn_data)
        pass
