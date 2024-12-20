from typing import Optional, Dict, Any,List
from pydantic import BaseModel
from models.source import SourceType


from enum import Enum

class ResultType(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILED"


class EventRequest(BaseModel):
    uuid: str
    source: SourceType
    url: str
    result: ResultType
    user_agent: Optional[str] = None
    ab_active: bool
    p_installed: Optional[List[str]] = None 
    payload: Dict[str, Any]  # Flexible payload that can be any structure
