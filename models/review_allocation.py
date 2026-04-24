class ReviewAllocation(Base):
    """
    ReviewAllocation Model: Handles split-payment logic for group contributions.
    
    In cases where a single large payment covers multiple people (e.g., a treasurer 
    paying for 5 members), this table tracks how the amount is split.
    """
    __tablename__ = "review_allocations"

    # Unique identifier for the allocation record
    allocation_id = Column(UUID, primary_key=True)
    # The associated pending transaction
    pending_id = Column(UUID)
    # The name of the specific member receiving this portion of the funds
    member_name = Column(String)
    # The currency amount assigned to this member
    allocated_amount = Column(Numeric)