# from dataclasses import dataclass

# @dataclass
# class Campaign:
#     id: str
#     name: str
#     goal: float
#     current_amount: float


class Campaign(Base):
    """
    Campaign Model: Represents a specific fundraising or savings goal.
    
    Examples: 'Welfare Fund', 'Investment Project A', 'End of Year Party'.
    All transactions in the system can optionally be mapped to a campaign
    to track progress against a target amount.
    """
    __tablename__ = "campaigns"

    # Unique identifier for the campaign
    campaign_id = Column(UUID, primary_key=True)
    # The group (tenant) this campaign belongs to
    group_id = Column(UUID)
    # Descriptive title of the goal
    title = Column(String)
    # The financial target to be reached
    target_amount = Column(Numeric)