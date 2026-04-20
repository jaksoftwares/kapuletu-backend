# from dataclasses import dataclass

# @dataclass
# class Campaign:
#     id: str
#     name: str
#     goal: float
#     current_amount: float


class Campaign(Base):
    __tablename__ = "campaigns"

    campaign_id = Column(UUID, primary_key=True)
    group_id = Column(UUID)
    title = Column(String)
    target_amount = Column(Numeric)