from sqlalchemy.orm import Session
from ..models import Client
from ..schemas import ClientCreate

def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def update_client(db: Session, client_id: int, client: ClientCreate):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client:
        db_client.name = client.name
        db_client.contact_person = client.contact_person
        db_client.phone = client.phone
        db_client.email = client.email
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client:
        db.delete(db_client)
        db.commit()
