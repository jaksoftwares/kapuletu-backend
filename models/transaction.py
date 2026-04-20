from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    amount: float
    sender_phone: str
    status: str  # pending, approved, rejected
    timestamp: str
