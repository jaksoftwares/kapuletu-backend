from pydantic import BaseModel

class IngestionSchema(BaseModel):
    message: str
    phone: str
