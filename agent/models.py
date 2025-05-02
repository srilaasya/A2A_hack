from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS_WITH_RESULT = "success_with_result"
    SUCCESS_WITHOUT_RESULT = "success_without_result"
    FAILED = "failed"

class TaskType(str, Enum):
    PROPERTY_SEARCH = "property_search"
    PROPERTY_UPDATE = "property_update"
    NOTION_SYNC = "notion_sync"
    EMAIL_UPDATE = "email_update"

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
    task_id: str = Field(..., description="Unique identifier for the task")
    task_type: TaskType = Field(..., description="Type of task to execute")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for the task execution"
    )

class TaskResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task")
    status: TaskStatus = Field(..., description="Status of the task execution")
    result: Optional[Dict[str, Any]] = Field(None, description="Result of the task execution")
    error_message: Optional[str] = Field(None, description="Error message if task failed")

class Property(BaseModel):
    address: str = Field(..., description="Property address")
    price: float = Field(..., description="Property price")
    bedrooms: int = Field(..., description="Number of bedrooms")
    bathrooms: float = Field(..., description="Number of bathrooms")
    property_type: str = Field(..., description="Type of property")
    source: str = Field(..., description="Source of the property data")
    url: Optional[str] = Field(None, description="URL to the property listing")
    notes: Optional[str] = Field(None, description="Additional notes about the property")

class NotionProperty(BaseModel):
    name: str = Field(..., description="Property name/address")
    price: float = Field(..., description="Property price")
    bedrooms: int = Field(..., description="Number of bedrooms")
    bathrooms: float = Field(..., description="Number of bathrooms")
    status: str = Field(..., description="Property status")
    source: str = Field(..., description="Source of the property data")
    url: Optional[str] = Field(None, description="URL to the property listing")
    notes: Optional[str] = Field(None, description="Additional notes about the property") 