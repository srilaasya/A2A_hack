# Realtor Agent

A realtor agent that helps users search for properties using real estate APIs.

## Features

- Property search using Oxxylabs (Zillow) and Attom APIs
- Task execution with progress streaming
- REST API interface

## Prerequisites

- Python 3.8 or higher
- Oxxylabs username and password
- Attom API key

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

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials:
# OXYLABS_USERNAME=your_username
# OXYLABS_PASSWORD=your_password
# ATTOM_API_KEY=your_attom_api_key
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

## API Integration

The agent integrates with two property data sources:

1. **Oxxylabs (Zillow)**
   - Provides real-time property listings
   - Requires OXYLABS_USERNAME and OXYLABS_PASSWORD

2. **Attom**
   - Provides detailed property information
   - Requires ATTOM_API_KEY

## Development

The project uses:
- FastAPI for the web server
- Pydantic for data validation
- Click for CLI interface
- httpx for async HTTP requests 