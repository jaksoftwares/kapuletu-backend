class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    password_hash = Column(String)
    role = Column(String)
    is_active = Column(Boolean)