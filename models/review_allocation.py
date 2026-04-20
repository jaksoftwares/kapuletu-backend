class ReviewAllocation(Base):
    __tablename__ = "review_allocations"

    allocation_id = Column(UUID, primary_key=True)
    pending_id = Column(UUID)
    member_name = Column(String)
    allocated_amount = Column(Numeric)