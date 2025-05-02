# Realtor Agent

A simple realtor agent that helps users search for properties.

## Features

- Property search functionality
- Task execution with progress streaming
- REST API interface

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package:
```bash
pip install -e .
```

## Usage

Run the agent server:
```bash
python -m realtor_agent.agent.__main__
```

The server will start on `http://localhost:10002`.

### API Endpoints

- `GET /` - Get the agent card
- `POST /execute` - Execute a task
- `POST /execute/stream` - Execute a task with progress streaming

### Example Task Request

```json
{
    "id": "test-task-1",
    "params": {
        "location": "San Francisco",
        "price_range": "$500k-$1M",
        "bedrooms": 2,
        "bathrooms": 2,
        "property_type": "condo"
    }
}
```

## Development

The project uses:
- FastAPI for the web server
- Pydantic for data validation
- Click for CLI interface 