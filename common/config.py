import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """
    Central configuration object for the KapuLetu Backend.
    Loads environment variables from the system (in Production) or a .env file (in Development).
    """
    # PostgreSQL connection string (e.g. postgresql://user:pass@host:port/db)
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Amazon QLDB Ledger name for immutable records
    QLDB_LEDGER_NAME: str = os.getenv("QLDB_LEDGER_NAME", "kapuletu-ledger")
    
    # Twilio Webhook Secret for signature validation (security layer)
    TWILIO_SECRET: str = os.getenv("TWILIO_SECRET")

def get_config() -> Config:
    """
    Returns a fresh instance of the configuration.
    Using a dataclass ensures type-safety and easy attribute access.
    """
    return Config()
