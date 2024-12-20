from typing import Optional, Dict, Any,List
from pydantic import BaseModel
from models.source import SourceType


class EventRequest(BaseModel):
    uuid: str
    source: SourceType
    url: str
    success: bool
    status: str
    user_agent: Optional[str] = None
    ab_active: bool
    p_installed: Optional[List[str]] = None 
    payload: Dict[str, Any]  # Flexible payload that can be any structure
