from pydantic import BaseModel

class ApprovalSchema(BaseModel):
    transaction_id: str
    action: str
