import os
import logging
from typing import List, Dict, Any
from notion_client import Client
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import pickle
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotionClient:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")

    async def get_properties(self) -> List[Dict[str, Any]]:
        """Fetch all properties from Notion database"""
        try:
            response = self.notion.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Status",
                    "select": {
                        "equals": "Active"
                    }
                }
            )
            return response.get("results", [])
        except Exception as e:
            logger.error(f"Error fetching properties from Notion: {e}")
            return []

    async def add_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new property to Notion database"""
        try:
            response = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Name": {"title": [{"text": {"content": property_data["address"]}}]},
                    "Price": {"number": property_data["price"]},
                    "Bedrooms": {"number": property_data["bedrooms"]},
                    "Bathrooms": {"number": property_data["bathrooms"]},
                    "Status": {"select": {"name": "Active"}},
                    "Source": {"select": {"name": property_data.get("source", "Zillow")}},
                    "URL": {"url": property_data.get("url", "")},
                    "Notes": {"rich_text": [{"text": {"content": property_data.get("notes", "")}}]}
                }
            )
            return response
        except Exception as e:
            logger.error(f"Error adding property to Notion: {e}")
            return {}

class ZillowClient:
    def __init__(self):
        self.base_url = "https://www.zillow.com"
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    async def search_properties(self, location: str, price_range: str, 
                              bedrooms: int, bathrooms: int) -> List[Dict[str, Any]]:
        """Search for properties on Zillow"""
        try:
            search_url = f"{self.base_url}/homes/{location}/"
            self.driver.get(search_url)
            
            # Wait for page to load and get results
            # Note: This is a simplified version. In production, you'd need to handle
            # pagination, filters, and proper waiting for elements
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            properties = []
            for listing in soup.find_all("div", class_="list-card-info"):
                try:
                    address = listing.find("address").text.strip()
                    price = listing.find("div", class_="list-card-price").text.strip()
                    details = listing.find("ul", class_="list-card-details").text.strip()
                    
                    properties.append({
                        "address": address,
                        "price": price,
                        "details": details,
                        "url": listing.find("a")["href"],
                        "source": "Zillow"
                    })
                except Exception as e:
                    logger.error(f"Error parsing Zillow listing: {e}")
                    continue
            
            return properties
        except Exception as e:
            logger.error(f"Error searching Zillow: {e}")
            return []

    def __del__(self):
        """Cleanup WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

class GmailClient:
    def __init__(self):
        self.creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self):
        """Get or refresh Gmail API credentials"""
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    ['https://www.googleapis.com/auth/gmail.send']
                )
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return creds

    async def send_property_update(self, to_email: str, properties: List[Dict[str, Any]]):
        """Send property updates via email"""
        try:
            message = MIMEMultipart()
            message['to'] = to_email
            message['subject'] = 'New Property Updates'

            # Create HTML content
            html_content = """
            <html>
                <body>
                    <h2>New Property Updates</h2>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
            """
            
            for prop in properties:
                html_content += f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
                        <h3>{prop['address']}</h3>
                        <p><strong>Price:</strong> {prop['price']}</p>
                        <p><strong>Details:</strong> {prop['details']}</p>
                        <a href="{prop['url']}" style="color: #1a73e8;">View on {prop['source']}</a>
                    </div>
                """
            
            html_content += """
                    </div>
                </body>
            </html>
            """

            message.attach(MIMEText(html_content, 'html'))
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            logger.info(f"Property update email sent to {to_email}")
        except Exception as e:
            logger.error(f"Error sending email: {e}") 