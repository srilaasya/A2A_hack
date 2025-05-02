from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
import uvicorn
import logging
import json
import traceback
from .models import AgentCard, TaskRequest, TaskResponse
from .task_manager import TaskManager

logger = logging.getLogger(__name__)

class A2AServer:
    def __init__(self, agent_card: AgentCard, host: str = "localhost", port: int = 10002):
        self.app = FastAPI()
        self.agent_card = agent_card
        self.host = host
        self.port = port
        self.task_manager = TaskManager()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        async def get_agent_card():
            return self.agent_card

        @self.app.post("/execute")
        async def execute_task(request: TaskRequest):
            try:
                result = await self.task_manager.execute_task(request)
                return TaskResponse(
                    id=request.id,
                    result=result
                )
            except Exception as e:
                logger.error(f"Error executing task: {e}\n{traceback.format_exc()}")
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e), "traceback": traceback.format_exc()}
                )

        @self.app.post("/execute/stream")
        async def execute_task_stream(request: TaskRequest):
            async def stream_generator():
                try:
                    async for result in self.task_manager.execute_task_stream(request):
                        yield json.dumps({"id": request.id, "result": result}) + "\n"
                except Exception as e:
                    error_info = {
                        "error": str(e),
                        "traceback": traceback.format_exc()
                    }
                    logger.error(f"Error in stream: {json.dumps(error_info)}")
                    yield json.dumps(error_info) + "\n"

            return StreamingResponse(
                stream_generator(),
                media_type="application/x-ndjson"
            )

    def start(self):
        logger.info(f"Starting A2A server on {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="debug") 