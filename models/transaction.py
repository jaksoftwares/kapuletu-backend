# from dataclasses import dataclass

# @dataclass
# class Transaction:
#     id: str
#     amount: float
#     sender_phone: str
#     status: str  # pending, approved, rejected
#     timestamp: str


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(UUID, primary_key=True)
    transaction_code = Column(String)
    total_amount = Column(Numeric)
    status = Column(String)