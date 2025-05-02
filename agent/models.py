from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class AgentCard(BaseModel):
    name: str
    description: str
    version: str
    url: str
    capabilities: Dict[str, bool]
    skills: List[Dict[str, Any]]
    defaultInputModes: List[str]
    defaultOutputModes: List[str]

class TaskRequest(BaseModel):
    id: str
    params: Dict[str, Any]

class TaskResponse(BaseModel):
    id: str
    result: Dict[str, Any] 