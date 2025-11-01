"""Activity and attraction research tools using external APIs"""
from langchain_core.tools import tool
from typing import Dict, List
import json
from mocks.activity_data import MOCK_ACTIVITIES, MOCK_DESTINATION_INFO  # Note: Mocks kept for reference but not used (APIs are primary source)
from data.apis import ACTIVITIES_API, DESTINATION_INFO_API
from utils.api_client import fetch_api_data

@tool
def search_activities(destination: str, interests: str = "", max_price: int = 200) -> str:
    """Search for activities and attractions at destination.
    
    Args:
        destination: Destination city (e.g., 'Paris', 'Bali', 'Tokyo')
        interests: User interests (e.g., 'food', 'history', 'adventure', 'culture')
        max_price: Maximum price per activity (default: 200)
    
    Returns:
        JSON string with available activities
    """
    print(f"\n🎯 Searching activities in {destination} (interests: {interests})")
    
    # Normalize destination
    dest_key = destination.upper()
    
    # Fetch from external API
    try:
        api_response = fetch_api_data(url=ACTIVITIES_API)
        # API returns destination-based structure: {"PARIS": [...], "BALI": [...], ...}
        activities = None
        
        # Find matching activities - try partial matching
        for key in api_response.keys():
            if key == "DEFAULT":
                continue
            if key in dest_key or dest_key in key:
                activities = api_response[key]
                break
        
        # Use default if no match
        if not activities and "DEFAULT" in api_response:
            activities = api_response["DEFAULT"]
        
        if not activities:
            activities = []
            
    except Exception as e:
        print(f"❌ Failed to fetch activities from API: {str(e)}")
        return json.dumps({
            "destination": destination,
            "total_found": 0,
            "activities": [],
            "message": f"Error fetching activities: {str(e)}"
        })
    
    # Filter by price
    filtered_activities = [a for a in activities if a.get("price", float('inf')) <= max_price]
    
    # Filter by interests if provided
    if interests:
        interest_keywords = interests.lower().split()
        interest_filtered = []
        for activity in filtered_activities:
            activity_text = (activity.get("name", "") + " " + activity.get("category", "") + " " + 
                           activity.get("description", "")).lower()
            if any(keyword in activity_text for keyword in interest_keywords):
                interest_filtered.append(activity)
        
        if interest_filtered:
            filtered_activities = interest_filtered
    
    result = {
        "destination": destination,
        "total_found": len(filtered_activities),
        "activities": filtered_activities[:6]  # Return top 6
    }
    
    return json.dumps(result)

@tool
def get_destination_info(destination: str) -> str:
    """Get general information about a destination including best time to visit, 
    visa requirements, safety tips, and local tips.
    
    Args:
        destination: Destination city or country
    
    Returns:
        Comprehensive destination information
    """
    print(f"\n📍 Getting destination info for {destination}")
    
    dest_key = destination.upper()
    
    # Fetch from external API
    try:
        api_response = fetch_api_data(url=DESTINATION_INFO_API)
        # API returns destination-based structure: {"PARIS": {...}, "BALI": {...}, ...}
        info = None
        
        # Try to match destination
        for key in api_response.keys():
            if key in dest_key or dest_key in key:
                info = api_response[key]
                break
        
        # Use default if no match
        if not info:
            info = {
                "best_time_to_visit": "Varies by region - research specific destination",
                "currency": "Local currency",
                "language": "Local language",
                "safety_tips": ["Research local safety information", "Register with embassy"],
                "local_tips": ["Research local customs", "Get travel insurance"]
            }
            
    except Exception as e:
        print(f"❌ Failed to fetch destination info from API: {str(e)}")
        info = {
            "best_time_to_visit": "Varies by region - research specific destination",
            "currency": "Local currency",
            "language": "Local language",
            "safety_tips": ["Research local safety information", "Register with embassy"],
            "local_tips": ["Research local customs", "Get travel insurance"],
            "error": f"Error fetching destination info: {str(e)}"
        }
    
    return json.dumps(info)

