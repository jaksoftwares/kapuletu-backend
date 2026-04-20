from dataclasses import dataclass

@dataclass
class LedgerEntry:
    id: str
    transaction_id: str
    checksum: str
    timestamp: str
