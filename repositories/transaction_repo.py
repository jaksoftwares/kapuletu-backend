from sqlalchemy.orm import Session
from sqlalchemy import select
from models.pending_transaction import PendingTransaction
from models.users import User
from uuid import UUID
from typing import List, Optional

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_pending_transaction(self, pending_txn: PendingTransaction) -> PendingTransaction:
        self.db.add(pending_txn)
        self.db.commit()
        self.db.refresh(pending_txn)
        return pending_txn

    def check_duplicate_transaction_code(self, transaction_code: str) -> bool:
        if not transaction_code:
            return False
        stmt = select(PendingTransaction).where(PendingTransaction.transaction_code == transaction_code)
        result = self.db.execute(stmt).scalars().first()
        return result is not None

    def resolve_owner_by_phone(self, phone_number: str) -> Optional[User]:
        """
        Identify the treasurer (owner) responsible for the incoming message number.
        """
        stmt = select(User).where(User.phone_number == phone_number)
        return self.db.execute(stmt).scalars().first()

    def fetch_pending_transactions_by_owner(self, owner_id: UUID) -> List[PendingTransaction]:
        stmt = select(PendingTransaction).where(
            PendingTransaction.owner_id == owner_id,
            PendingTransaction.is_processed == False
        )
        return self.db.execute(stmt).scalars().all()
