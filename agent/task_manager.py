import logging
import asyncio
from typing import Dict, Any, AsyncGenerator
from .models import TaskRequest, TaskResponse, TaskStatus
from .api_clients import AttomClient
from .integrations import NotionClient, ZillowClient, GmailClient

logger = logging.getLogger(__name__)

class TaskManager:
    """Manages property search tasks."""
    
    def __init__(self):
        self.attom_client = AttomClient()
        self.notion_client = NotionClient()
        self.zillow_client = ZillowClient()
        self.gmail_client = GmailClient()
    
    async def execute_task(self, task_request: TaskRequest) -> TaskResponse:
        """Execute a task and return its result."""
        try:
            # Get parameters from task request
            location = task_request.parameters.get("location", "")
            price_range = task_request.parameters.get("price_range", "$500k-$1M")
            bedrooms = task_request.parameters.get("bedrooms", 2)
            bathrooms = task_request.parameters.get("bathrooms", 2)
            property_type = task_request.parameters.get("property_type", "condo")
            email = task_request.parameters.get("email", "")

            # Search properties from multiple sources
            attom_properties = await self.attom_client.search_properties(
                location=location,
                price_range=price_range,
                bedrooms=bedrooms,
                bathrooms=bathrooms
            )

            zillow_properties = await self.zillow_client.search_properties(
                location=location,
                price_range=price_range,
                bedrooms=bedrooms,
                bathrooms=bathrooms
            )

            # Combine and deduplicate properties
            all_properties = self._combine_properties(attom_properties, zillow_properties)

            # Add properties to Notion database
            for property_data in all_properties:
                await self.notion_client.add_property(property_data)

            # Send email update if email provided
            if email and all_properties:
                await self.gmail_client.send_property_update(email, all_properties)

            return TaskResponse(
                task_id=task_request.task_id,
                status=TaskStatus.SUCCESS_WITH_RESULT,
                result=all_properties
            )

        except Exception as e:
            logger.error(f"Error executing task: {e}")
            return TaskResponse(
                task_id=task_request.task_id,
                status=TaskStatus.FAILED,
                error_message=str(e)
            )

    async def execute_task_stream(self, task_request: TaskRequest) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a task and stream its progress."""
        try:
            # Get parameters from task request
            location = task_request.parameters.get("location", "")
            price_range = task_request.parameters.get("price_range", "$500k-$1M")
            bedrooms = task_request.parameters.get("bedrooms", 2)
            bathrooms = task_request.parameters.get("bathrooms", 2)
            property_type = task_request.parameters.get("property_type", "condo")
            email = task_request.parameters.get("email", "")

            # Stream progress updates
            yield {"status": "searching", "message": "Searching Attom API..."}
            attom_properties = await self.attom_client.search_properties(
                location=location,
                price_range=price_range,
                bedrooms=bedrooms,
                bathrooms=bathrooms
            )

            yield {"status": "searching", "message": "Searching Zillow..."}
            zillow_properties = await self.zillow_client.search_properties(
                location=location,
                price_range=price_range,
                bedrooms=bedrooms,
                bathrooms=bathrooms
            )

            # Combine and deduplicate properties
            all_properties = self._combine_properties(attom_properties, zillow_properties)

            yield {"status": "processing", "message": "Updating Notion database..."}
            for property_data in all_properties:
                await self.notion_client.add_property(property_data)

            if email and all_properties:
                yield {"status": "processing", "message": "Sending email update..."}
                await self.gmail_client.send_property_update(email, all_properties)

            yield {
                "status": "completed",
                "message": "Task completed successfully",
                "result": all_properties
            }

        except Exception as e:
            logger.error(f"Error in task stream: {e}")
            yield {
                "status": "error",
                "message": str(e)
            }

    def _combine_properties(self, attom_properties: list, zillow_properties: list) -> list:
        """Combine and deduplicate properties from different sources"""
        combined = []
        seen_addresses = set()

        for prop in attom_properties + zillow_properties:
            address = prop.get("address", "").lower()
            if address and address not in seen_addresses:
                seen_addresses.add(address)
                combined.append(prop)

        return combined

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get the status and result of a task."""
        if task_id not in self.tasks:
            return None
        return self.tasks[task_id]
    
    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel a running task."""
        if task_id not in self.tasks:
            return {"status": "error", "message": f"Task {task_id} not found"}
        
        if self.tasks[task_id]["status"] == "running":
            self.tasks[task_id]["status"] = "cancelled"
            return {"status": "success", "message": f"Task {task_id} cancelled"}
        
        return {"status": "error", "message": f"Task {task_id} is not running"} 