from fastapi import Depends, FastAPI , HTTPException, status
from app.models import LoanDB,Base
from app.database import engine
from app.schemas import LoanCreate,LoanRead
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db


Loans: list[LoanCreate]=[]



app = FastAPI(title="Equipment Loan Service")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.post("/api/loans",response_model= LoanRead, status_code = status.HTTP_201_CREATED)
def add_loan(new_loan:LoanCreate,db:Session=Depends(get_db)):
    db_loan = LoanDB(**new_loan.model_dump())
    db.add(db_loan)

    try:
        db.commit()
        db.refresh(new_loan)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = "A loan with this equiptment id already exists")
    return db_loan

@app.get("/api/loans/{id}",response_model= LoanRead)
def get_loan(id:int,db:Session=Depends(get_db)):
    db_loan = db.get(LoanDB, id)

    if db_loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Loan not found")

    return db_loan


@app.delete("/api/loans/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(id: int, db:Session=Depends(get_db)):
    db_loan = db.get(LoanDB,id)

    if db_loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    db.delete(db_loan)
    db.commit()
    return
