"""Hotel search tools using external APIs"""
from langchain_core.tools import tool
from typing import Dict, List
import json
from urllib.parse import urlencode
from mocks.hotel_data import MOCK_HOTELS  # Note: Mocks kept for reference but not used (API is primary source)
from data.apis import HOTELS_API
from utils.api_client import fetch_api_data

@tool
def search_hotels(destination: str, check_in: str, check_out: str, guests: int = 2, 
                  min_stars: int = 3, max_price_per_night: int = 300) -> str:
    """Search for hotels at the destination.
    
    Args:
        destination: Destination city (e.g., 'Paris', 'Bali', 'Tokyo')
        check_in: Check-in date in format YYYY-MM-DD
        check_out: Check-out date in format YYYY-MM-DD
        guests: Number of guests (default: 2)
        min_stars: Minimum star rating (default: 3)
        max_price_per_night: Maximum price per night (default: 300)
    
    Returns:
        JSON string with available hotel options
    """
    print(f"\n🏨 Searching hotels in {destination} from {check_in} to {check_out} for {guests} guests")
    
    # Normalize destination
    dest_key = destination.upper()
    
    # Fetch from external API
    try:
        # Add query params to URL for demo purposes (responses won't change but shows proper API usage)
        query_params = urlencode({
            "location": destination,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests
        })
        api_url = f"{HOTELS_API}?{query_params}"
        api_response = fetch_api_data(url=api_url)
        # API returns destination-based structure: {"PARIS": [...], "BALI": [...], ...}
        hotels = None
        
        # Find matching hotels - try partial matching
        for key in api_response.keys():
            if key == "DEFAULT":
                continue
            if key in dest_key or dest_key in key:
                hotels = api_response[key]
                break
        
        # Use default if no match
        if not hotels and "DEFAULT" in api_response:
            hotels = api_response["DEFAULT"]
        
        if not hotels:
            hotels = []
            
    except Exception as e:
        print(f"❌ Failed to fetch hotels from API: {str(e)}")
        return json.dumps({
            "search_params": {
                "destination": destination,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests
            },
            "hotels": [],
            "message": f"Error fetching hotels: {str(e)}"
        })
    
    # Filter by criteria
    filtered_hotels = [
        h for h in hotels 
        if h.get("stars", 0) >= min_stars and h.get("price_per_night", float('inf')) <= max_price_per_night
    ]
    
    # Calculate nights and total
    from datetime import datetime
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (check_out_date - check_in_date).days
    
    result = {
        "search_params": {
            "destination": destination,
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "guests": guests
        },
        "hotels": [],
        "message": ""
    }
    
    if not filtered_hotels:
        result["message"] = f"No hotels found in {destination} matching your criteria."
    else:
        for hotel in filtered_hotels[:4]:  # Return top 4 options
            hotel_copy = hotel.copy()
            hotel_copy["nights"] = nights
            hotel_copy["total_price"] = hotel.get("price_per_night", 0) * nights
            result["hotels"].append(hotel_copy)
    
    return json.dumps(result)

@tool
def get_hotel_details(hotel_name: str) -> str:
    """Get detailed information about a specific hotel.
    
    Args:
        hotel_name: Name of the hotel
    
    Returns:
        Detailed hotel information
    """
    details = {
        "hotel_name": hotel_name,
        "check_in_time": "15:00",
        "check_out_time": "11:00",
        "cancellation_policy": "Free cancellation up to 24 hours before check-in",
        "payment_options": ["Credit Card", "Debit Card", "PayPal"],
        "languages_spoken": ["English", "Local Language"],
        "nearby_attractions": [
            "Tourist Attraction 1 - 500m",
            "Restaurant Area - 200m",
            "Metro Station - 300m"
        ],
        "room_types": {
            "standard": "Available",
            "deluxe": "Available (+$50/night)",
            "suite": "Available (+$150/night)"
        }
    }
    
    return json.dumps(details)

