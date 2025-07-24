from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Client, ClientCreate
from ..services import client_service

router = APIRouter(prefix="/api/clients", tags=["Clients"])

@router.post("", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return client_service.create_client(db, client)

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    db_client = client_service.get_client(db, client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    db_client = client_service.update_client(db, client_id, client)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client_service.delete_client(db, client_id)
