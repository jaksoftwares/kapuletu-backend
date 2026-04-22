from sqlalchemy import Column, String, UUID, Numeric, Text, Boolean, DateTime
from .users import Base
import datetime
import uuid

class PendingTransaction(Base):
    __tablename__ = "pending_transactions"

    pending_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), nullable=True) # Initially might be unknown until parsed
    group_id = Column(UUID(as_uuid=True), nullable=True)
    
    raw_text = Column(Text, nullable=False)
    amount = Column(Numeric(12, 2))
    sender_phone = Column(String)
    transaction_code = Column(String)
    
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)