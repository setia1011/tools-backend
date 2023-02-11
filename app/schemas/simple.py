from pydantic import BaseModel
from typing import Optional


class Simple(BaseModel):
    data: str
