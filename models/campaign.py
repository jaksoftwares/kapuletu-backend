from dataclasses import dataclass

@dataclass
class Campaign:
    id: str
    name: str
    goal: float
    current_amount: float
