class PendingTransaction(Base):
    __tablename__ = "pending_transactions"

    pending_id = Column(UUID, primary_key=True)
    owner_id = Column(UUID)
    group_id = Column(UUID)

    raw_message = Column(Text)
    extracted_amount = Column(Numeric)

    workflow_status = Column(String)