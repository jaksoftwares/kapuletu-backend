from sqlalchemy import Column, String, UUID, Numeric, Text, Boolean, DateTime, Float
from .users import Base
import datetime
import uuid

class PendingTransaction(Base):
    __tablename__ = "pending_transactions"

    pending_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), nullable=False) # Treasurer
    group_id = Column(UUID(as_uuid=True), nullable=True)
    campaign_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Raw Data
    raw_message = Column(Text, nullable=False)
    
    # Parsed Data
    sender_name = Column(String, nullable=True)
    amount = Column(Numeric(12, 2), nullable=True)
    currency = Column(String, default="KES")
    transaction_code = Column(String, unique=True, nullable=True)
    sender_phone = Column(String, nullable=True) # Extracted from message body
    purpose = Column(String, nullable=True)
    
    # Meta
    confidence_score = Column(Float, default=0.0)
    workflow_status = Column(String, default="pending") # pending, approved, rejected, edited
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)