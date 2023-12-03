from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime

class Response(BaseModel):
    message: Optional[str] = None
    jwt: Optional[str] = None 
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None 
    last_name: Optional[str] = None