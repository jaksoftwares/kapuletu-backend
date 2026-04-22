from sqlalchemy import Column, String, UUID, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="treasurer") # admin, treasurer, super_admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")
    groups = relationship("Group", back_populates="owner")