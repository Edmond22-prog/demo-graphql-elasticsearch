from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Category(BaseModel):
    uuid: str
    name: str
    normalized_name: str
    created_at: Optional[datetime] = None
