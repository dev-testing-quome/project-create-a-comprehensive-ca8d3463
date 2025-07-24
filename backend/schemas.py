from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class User(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class ClientCreate(BaseModel):
    name: str
    contact_person: str
    phone: str
    email: str

class Client(BaseModel):
    id: int
    name: str
    contact_person: str
    phone: str
    email: str
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class CaseCreate(BaseModel):
    client_id: int
    case_name: str
    description: Optional[str] = None
    status: str = "open"
    court_date: Optional[datetime] = None

class Case(BaseModel):
    id: int
    client_id: int
    case_name: str
    description: Optional[str] = None
    status: str
    court_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    client: Client
    documents: List["Document"] = []
    class Config:
        orm_mode = True

class DocumentCreate(BaseModel):
    case_id: int
    file_path: str
    description: Optional[str] = None

class Document(BaseModel):
    id: int
    case_id: int
    file_path: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
