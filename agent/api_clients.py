import os
import logging
import httpx
import base64
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class OxxylabsClient:
    def __init__(self):
        self.username = os.getenv("OXYLABS_USERNAME")
        self.password = os.getenv("OXYLABS_PASSWORD")
        self.base_url = "https://realtime.oxylabs.io/v1/queries"
        if not self.username or not self.password:
            raise ValueError("OXYLABS_USERNAME and OXYLABS_PASSWORD environment variables not set")

    async def search_properties(self, location: str, price_range: str, 
                              bedrooms: int, bathrooms: int, 
                              property_type: str) -> Dict[str, Any]:
        """Search for properties using Oxxylabs."""
        try:
            # Format the Zillow URL with search parameters
            search_url = f"https://www.zillow.com/homes/{location.replace(' ', '-')}/"
            if price_range:
                min_price = price_range.split("-")[0].strip("$k").strip("$M")
                max_price = price_range.split("-")[1].strip("$k").strip("$M")
                min_price = float(min_price) * (1000 if "k" in price_range.lower() else 1000000)
                max_price = float(max_price) * (1000 if "k" in price_range.lower() else 1000000)
                search_url += f"price-{int(min_price)}-{int(max_price)}_price/"
            if bedrooms:
                search_url += f"{bedrooms}-_beds/"
            if bathrooms:
                search_url += f"{bathrooms}-_baths/"
            if property_type and property_type.lower() != "any":
                search_url += f"type-{property_type}/"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    auth=(self.username, self.password),
                    json={
                        "source": "universal",
                        "url": search_url,
                        "geo_location": "United States",
                        "render": "html",
                        "parse": True,
                        "parsing_instructions": {
                            "listings": {
                                "_fns": [
                                    {
                                        "_fn": "xpath",
                                        "_args": ["//article[contains(@class, 'list-card')]"]
                                    }
                                ],
                                "price": "//span[contains(@class, 'price')]/text()",
                                "address": "//address/text()",
                                "beds": "//ul[contains(@class, 'property-facts')]//li[contains(text(), 'bed')]/text()",
                                "baths": "//ul[contains(@class, 'property-facts')]//li[contains(text(), 'bath')]/text()",
                                "sqft": "//ul[contains(@class, 'property-facts')]//li[contains(text(), 'sqft')]/text()"
                            }
                        }
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error searching properties with Oxxylabs: {e}")
            raise

class AttomClient:
    def __init__(self):
        self.api_key = os.getenv("ATTOM_API_KEY")
        self.base_url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0"
        if not self.api_key:
            raise ValueError("ATTOM_API_KEY environment variable not set")

    async def search_by_address(self, address: str) -> Dict[str, Any]:
        """Search for properties by address."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/property/address",
                    headers={
                        "Accept": "application/json",
                        "APIKey": self.api_key
                    },
                    params={
                        "address": address,
                        "page": 1,
                        "pagesize": 10
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error searching properties by address: {e}")
            raise

    async def search_properties(self, location: str, price_range: str,
                              bedrooms: int, bathrooms: int,
                              property_type: str) -> Dict[str, Any]:
        """Search for properties using Attom."""
        try:
            # Use the address search endpoint
            return await self.search_by_address(location)
        except Exception as e:
            logger.error(f"Error searching properties with Attom: {e}")
            raise 