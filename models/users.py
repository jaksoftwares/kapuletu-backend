from sqlalchemy import Column, String, UUID, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime
import uuid

Base = declarative_base()

class User(Base):
    """
    User Model: Represents the core identity for Treasurers and Admins.
    
    This is the top-level entity in the KapuLetu ecosystem. 
    A user (typically a treasurer) manages community groups and is the 
    authorizing entity for financial transactions ingested into the system.
    """
    __tablename__ = "users"

    # Unique identifier for the user (UUID)
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Personal Information
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Primary identifier for incoming webhook messages (Twilio/WhatsApp)
    phone_number = Column(String, unique=True, nullable=False)
    
    # Security: Hashed password (never stored in plain text)
    password_hash = Column(String, nullable=False)
    
    # Permissions Role: Controls access to specific dashboard features
    # - treasurer: Manages specific groups
    # - admin: Platform-level management
    # - super_admin: Infrastructure control
    role = Column(String, default="treasurer") 
    
    # Account Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    # A user can have multiple active feature subscriptions
    subscriptions = relationship("Subscription", back_populates="user")
    # A treasurer can own and manage multiple community groups
    groups = relationship("Group", back_populates="owner")