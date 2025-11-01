"""Hotel search tools with mocked API responses"""
from langchain_core.tools import tool
from typing import Dict, List
import json
from mocks.hotel_data import MOCK_HOTELS

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
    
    # Find matching hotels - try partial matching
    hotels = None
    for key in MOCK_HOTELS.keys():
        if key == "DEFAULT":
            continue
        if key in dest_key or dest_key in key:
            hotels = MOCK_HOTELS[key]
            break
    
    # Use default if no match
    if not hotels:
        hotels = MOCK_HOTELS["DEFAULT"]
    
    # Filter by criteria
    filtered_hotels = [
        h for h in hotels 
        if h["stars"] >= min_stars and h["price_per_night"] <= max_price_per_night
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
            hotel_copy["total_price"] = hotel["price_per_night"] * nights
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

