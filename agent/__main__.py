import logging
import click
from .a2a_server import A2AServer
from .models import AgentCard

logger = logging.getLogger(__name__)

def create_agent_card() -> AgentCard:
    """Create the agent card with capabilities and skills."""
    return AgentCard(
        name="Realtor Agent",
        description="An agent that helps users search for properties",
        version="1.0.0",
        url="http://localhost:10002",
        capabilities={
            "property_search": True
        },
        skills=[
            {
                "name": "property_search",
                "description": "Search for properties based on various criteria",
                "parameters": {
                    "location": "string",
                    "price_range": "string",
                    "bedrooms": "integer",
                    "bathrooms": "integer",
                    "property_type": "string"
                }
            }
        ],
        defaultInputModes=["text"],
        defaultOutputModes=["text", "json"]
    )

@click.command()
@click.option('--host', default='localhost', help='Host to run the server on')
@click.option('--port', default=10002, help='Port to run the server on')
def main(host: str, port: int):
    """Run the Realtor Agent server."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        # Create agent card
        agent_card = create_agent_card()
        
        # Create and start server
        server = A2AServer(agent_card, host=host, port=port)
        server.start()
        
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        raise

if __name__ == "__main__":
    main() 