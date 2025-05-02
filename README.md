# Realtor Agent

A powerful real estate agent powered by AI that integrates with multiple data sources and tools to provide comprehensive property search and management capabilities.

## Features

- **Multi-Source Property Search**
  - Attom API integration for property data
  - Zillow web scraping for additional listings
  - Property deduplication across sources

- **Notion Integration**
  - Automatic property database management
  - Real-time updates to your Notion workspace
  - Customizable property fields and status tracking

- **Email Notifications**
  - Gmail integration for property updates
  - Beautiful HTML email templates
  - Customizable notification preferences

- **Modern UI**
  - Real-time search results
  - Interactive property cards
  - Visual workflow tracking
  - Responsive design

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Notion account
- Gmail account
- Attom API key
- Zillow account (for web scraping)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd realtor_agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -e .
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your API keys and credentials:
   ```
   ATTOM_API_KEY=your_attom_api_key
   NOTION_API_KEY=your_notion_api_key
   NOTION_DATABASE_ID=your_database_id
   GMAIL_CLIENT_ID=your_client_id
   GMAIL_CLIENT_SECRET=your_client_secret
   ZILLOW_USER_AGENT=your_user_agent
   ```

5. Set up Notion:
   - Create a new database in Notion
   - Add the following properties:
     - Name (title)
     - Price (number)
     - Bedrooms (number)
     - Bathrooms (number)
     - Status (select)
     - Source (select)
     - URL (url)
     - Notes (rich text)
   - Get your database ID from the URL
   - Create an integration at https://www.notion.so/my-integrations
   - Share your database with the integration

6. Set up Gmail:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download the credentials file as `credentials.json`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install --legacy-peer-deps
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Start the backend server:
   ```bash
   python -m realtor_agent
   ```

2. Open your browser to `http://localhost:3000`

3. Enter your search criteria:
   - Location
   - Price range
   - Number of bedrooms
   - Number of bathrooms
   - Property type

4. The agent will:
   - Search multiple sources for matching properties
   - Update your Notion database with new listings
   - Send email updates if configured
   - Display results in real-time

## Architecture

The application follows a modern microservices architecture:

- **Backend**: FastAPI-based Python server
  - Task management system
  - API integrations
  - Data processing and deduplication

- **Frontend**: React-based web application
  - Real-time updates
  - Interactive UI
  - Responsive design

- **Integrations**:
  - Notion: Property database management
  - Gmail: Email notifications
  - Zillow: Web scraping for listings
  - Attom: Property data API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 