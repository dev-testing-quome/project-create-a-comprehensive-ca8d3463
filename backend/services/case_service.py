from sqlalchemy.orm import Session
from ..models import Case
from ..schemas import CaseCreate

def create_case(db: Session, case: CaseCreate):
    db_case = Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

def get_case(db: Session, case_id: int):
    return db.query(Case).filter(Case.id == case_id).first()

def update_case(db: Session, case_id: int, case: CaseCreate):
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if db_case:
        db_case.case_name = case.case_name
        db_case.description = case.description
        db_case.status = case.status
        db_case.court_date = case.court_date
        db.commit()
        db.refresh(db_case)
    return db_case

def delete_case(db: Session, case_id: int):
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if db_case:
        db.delete(db_case)
        db.commit()
