from sqlalchemy import Column, String, JSON, DateTime
from .users import Base
import datetime

class ParserKnowledge(Base):
    """
    The permanent memory of the Ingestion AI.
    Stores structural fingerprints and their successful mappings 
    confirmed by treasurers.
    """
    __tablename__ = "parser_knowledge_base"

    # The fingerprint represents the 'shape' of a message (e.g., 'UPPER word NUM for word')
    fingerprint = Column(String, primary_key=True)
    
    # Mapping logic: index positions of tokens for name, amount, etc.
    # e.g., {"sender_name_indices": [0], "amount_index": 2}
    mapping_logic = Column(JSON, nullable=False)
    
    occurrence_count = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    success_count = Column(DateTime, default=datetime.datetime.utcnow) # Track reliability
