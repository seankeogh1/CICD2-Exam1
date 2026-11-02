from typing import Annotated

from pydantic import BaseModel,ConfigDict,Field,StringConstraints


class LoanCreate(BaseModel):
    equipment_id: int = Field(gt=0)
    borrower_name: str = Field(min_length=2,max_length=60)
    loan_days: int = Field(ge=1,le=14)
    purpose: str = Field(min_length=5,max_length=100)



class LoanRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    equipment_id: int
    borrower_name: str
    loan_days: int
    purpose: str


