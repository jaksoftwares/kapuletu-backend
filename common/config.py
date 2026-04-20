import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    QLDB_LEDGER_NAME: str = os.getenv("QLDB_LEDGER_NAME", "kapuletu-ledger")
    TWILIO_SECRET: str = os.getenv("TWILIO_SECRET")

def get_config():
    return Config()
