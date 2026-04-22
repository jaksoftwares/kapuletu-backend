from sqlalchemy import Column, String, UUID, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .users import Base
import datetime
import uuid

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.group_id"), nullable=False)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.campaign_id"), nullable=True)
    transaction_code = Column(String, unique=True, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    sender_phone = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected, voided
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    allocations = relationship("ReviewAllocation", back_populates="transaction")