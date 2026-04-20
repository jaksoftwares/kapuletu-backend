class Group(Base):
    __tablename__ = "groups"

    group_id = Column(UUID, primary_key=True)
    owner_id = Column(UUID)
    group_name = Column(String)
    currency = Column(String)