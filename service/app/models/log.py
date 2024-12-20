from typing import Optional, Dict, Any,List
from pydantic import BaseModel
from models.source import SourceType

from enum import Enum

class LogRequest(BaseModel):
    uuid: str
    logs: Optional[List[str]] = None
    title : Optional[str] = None
    source: SourceType
