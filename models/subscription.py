from sqlalchemy import Column, String, UUID, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from .users import Base
import datetime
import uuid

class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False) # Free trial, Basic, Pro, Enterprise
    max_groups = Column(Integer, default=1)
    max_campaigns = Column(Integer, default=5)
    max_transactions_per_month = Column(Integer, default=100)
    price = Column(Integer, default=0) # In local currency units

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.plan_id"), nullable=False)
    status = Column(String, default="active") # active, expired, suspended
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)
    is_auto_renew = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscriptions")

class UsageTracking(Base):
    __tablename__ = "usage_tracking"

    usage_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    metric_name = Column(String, nullable=False) # e.g., "transactions_this_month"
    current_value = Column(Integer, default=0)
    last_reset = Column(DateTime, default=datetime.datetime.utcnow)
