from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Response(BaseModel):
    message: Optional[str] = None
    url: Optional[str] = None