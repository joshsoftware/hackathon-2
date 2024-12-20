from typing import Optional, Dict, List
from pydantic import BaseModel
from models.source import SourceType

class LogRequest(BaseModel):
    uuid: str
    logs: Optional[List[str]] = None
    title : Optional[str] = None
    source: SourceType
