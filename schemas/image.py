from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Response(BaseModel):
    message: Optional[str]
    url: Optional[str]