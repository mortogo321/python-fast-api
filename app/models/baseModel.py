from typing import Optional

from pydantic import BaseModel


class Response(BaseModel):
    success:bool
    message: str
    errors: Optional[dict] = None
