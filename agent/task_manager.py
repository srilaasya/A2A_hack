import logging
import asyncio
from typing import Dict, Any, AsyncGenerator
from .models import TaskRequest
from .api_clients import OxxylabsClient, AttomClient

logger = logging.getLogger(__name__)

class TaskManager:
    """Manages property search tasks."""
    
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.task_results: Dict[str, Dict[str, Any]] = {}
        self.attom_client = AttomClient()
    
    async def execute_task(self, request: TaskRequest) -> Dict[str, Any]:
        """Execute a task and return its result."""
        try:
            # Store the task
            self.tasks[request.id] = {
                "params": request.params,
                "status": "running"
            }

            # Get parameters
            params = request.params
            location = params.get("location")
            price_range = params.get("price_range")
            bedrooms = params.get("bedrooms")
            bathrooms = params.get("bathrooms")
            property_type = params.get("property_type")

            # Search properties using Attom API only
            attom_results = await self.attom_client.search_properties(
                location, price_range, bedrooms, bathrooms, property_type
            )

            # Format results
            result = {
                "status": "completed",
                "data": {
                    "attom_results": attom_results
                }
            }

            # Store the result
            self.task_results[request.id] = result
            self.tasks[request.id]["status"] = "completed"

            return result

        except Exception as e:
            logger.error(f"Error executing task {request.id}: {e}")
            self.tasks[request.id]["status"] = "failed"
            self.tasks[request.id]["error"] = str(e)
            raise

    async def execute_task_stream(self, request: TaskRequest) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a task and stream its progress."""
        try:
            # Store the task
            self.tasks[request.id] = {
                "params": request.params,
                "status": "running"
            }

            # Get parameters
            params = request.params
            location = params.get("location")
            price_range = params.get("price_range")
            bedrooms = params.get("bedrooms")
            bathrooms = params.get("bathrooms")
            property_type = params.get("property_type")

            # Stream progress updates
            yield {
                "status": "in_progress",
                "progress": 20,
                "message": "Starting property search..."
            }

            # Search Attom
            yield {
                "status": "in_progress",
                "progress": 60,
                "message": "Searching Attom database..."
            }
            attom_results = await self.attom_client.search_properties(
                location, price_range, bedrooms, bathrooms, property_type
            )

            # Process results
            yield {
                "status": "in_progress",
                "progress": 80,
                "message": "Processing results..."
            }

            # Final result
            result = {
                "status": "completed",
                "data": {
                    "attom_results": attom_results
                }
            }

            # Store the result
            self.task_results[request.id] = result
            self.tasks[request.id]["status"] = "completed"

            yield result

        except Exception as e:
            logger.error(f"Error executing task stream {request.id}: {e}")
            self.tasks[request.id]["status"] = "failed"
            self.tasks[request.id]["error"] = str(e)
            raise

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