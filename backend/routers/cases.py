from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Case, CaseCreate
from ..services import case_service

router = APIRouter(prefix="/api/cases", tags=["Cases"])

@router.post("", response_model=Case, status_code=status.HTTP_201_CREATED)
def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    return case_service.create_case(db, case)

@router.get("/{case_id}", response_model=Case)
def get_case(case_id: int, db: Session = Depends(get_db)):
    db_case = case_service.get_case(db, case_id)
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return db_case

@router.put("/{case_id}", response_model=Case)
def update_case(case_id: int, case: CaseCreate, db: Session = Depends(get_db)):
    db_case = case_service.update_case(db, case_id, case)
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return db_case

@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: int, db: Session = Depends(get_db)):
    case_service.delete_case(db, case_id)
