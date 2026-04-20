class ReviewAction(Base):
    __tablename__ = "review_actions"

    action_id = Column(UUID, primary_key=True)
    pending_id = Column(UUID)
    action_type = Column(String)