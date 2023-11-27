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
    message: Optional[str]
    jwt: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]