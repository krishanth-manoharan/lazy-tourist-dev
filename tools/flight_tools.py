"""Flight search tools with mocked API responses"""
from langchain_core.tools import tool
from typing import Dict, List
import json
from mocks.flight_data import MOCK_FLIGHTS, MOCK_RETURN_FLIGHTS

@tool
def search_flights(origin: str, destination: str, departure_date: str, passengers: int = 2, max_price: int = 2000) -> str:
    """Search for flights between origin and destination.
    
    Args:
        origin: Departure city or airport code (e.g., 'NYC', 'JFK')
        destination: Arrival city or destination (e.g., 'Paris', 'Bali', 'Tokyo')
        departure_date: Departure date in format YYYY-MM-DD
        passengers: Number of passengers (default: 2)
        max_price: Maximum price per person (default: 2000)
    
    Returns:
        JSON string with available flight options
    """
    print(f"\n🛫 Searching flights: {origin} → {destination} for {passengers} passengers on {departure_date}")
    
    # Normalize inputs
    origin_key = origin.upper()
    dest_key = destination.upper()
    
    # Find matching flights
    search_key = f"{origin_key}-{dest_key}"
    flights = None
    
    # Try exact match first
    if search_key in MOCK_FLIGHTS:
        flights = MOCK_FLIGHTS[search_key]
    else:
        # Try partial matches - check if destination contains any known city
        for key in MOCK_FLIGHTS.keys():
            if key == "DEFAULT":
                continue
            # Extract destination from key (format: ORIGIN-DEST)
            if "-" in key:
                _, key_dest = key.split("-", 1)
                if key_dest in dest_key or dest_key in key_dest:
                    flights = MOCK_FLIGHTS[key]
                    break
    
    # Use default if no match
    if not flights:
        flights = MOCK_FLIGHTS["DEFAULT"]
    
    # Filter by price and format response
    filtered_flights = [f for f in flights if f["price"] <= max_price]
    
    # Calculate total prices
    result = {
        "search_params": {
            "origin": origin,
            "destination": destination,
            "date": departure_date,
            "passengers": passengers
        },
        "flights": [],
        "message": ""
    }
    
    if not filtered_flights:
        result["message"] = f"No flights found from {origin} to {destination} under ${max_price} per person."
    else:
        for flight in filtered_flights[:3]:  # Return top 3 options
            flight_copy = flight.copy()
            flight_copy["total_price"] = flight["price"] * passengers
            flight_copy["price_per_person"] = flight["price"]
            result["flights"].append(flight_copy)
    
    return json.dumps(result)

@tool
def search_return_flights(origin: str, destination: str, return_date: str, passengers: int = 2, max_price: int = 2000) -> str:
    """Search for return flights from destination back to origin.
    
    Args:
        origin: Original departure city (where to return to)
        destination: Current location (where returning from)
        return_date: Return date in format YYYY-MM-DD
        passengers: Number of passengers (default: 2)
        max_price: Maximum price per person (default: 2000)
    
    Returns:
        JSON string with available return flight options
    """
    print(f"\n🛬 Searching return flights: {destination} → {origin} for {passengers} passengers on {return_date}")
    
    # Normalize inputs (reverse direction for return)
    origin_key = origin.upper()
    dest_key = destination.upper()
    
    # Find matching return flights (destination to origin)
    search_key = f"{dest_key}-{origin_key}"
    flights = None
    
    # Try exact match first
    if search_key in MOCK_RETURN_FLIGHTS:
        flights = MOCK_RETURN_FLIGHTS[search_key]
    else:
        # Try partial matches
        for key in MOCK_RETURN_FLIGHTS.keys():
            if key == "DEFAULT":
                continue
            if "-" in key:
                key_origin, _ = key.split("-", 1)
                if key_origin in dest_key or dest_key in key_origin:
                    flights = MOCK_RETURN_FLIGHTS[key]
                    break
    
    # Use default if no match
    if not flights:
        flights = MOCK_RETURN_FLIGHTS["DEFAULT"]
    
    # Filter by price and format response
    filtered_flights = [f for f in flights if f["price"] <= max_price]
    
    # Calculate total prices
    result = {
        "search_params": {
            "origin": destination,  # Returning from destination
            "destination": origin,  # Returning to origin
            "date": return_date,
            "passengers": passengers
        },
        "flights": [],
        "message": ""
    }
    
    if not filtered_flights:
        result["message"] = f"No return flights found from {destination} to {origin} under ${max_price} per person."
    else:
        for flight in filtered_flights[:3]:  # Return top 3 options
            flight_copy = flight.copy()
            flight_copy["total_price"] = flight["price"] * passengers
            flight_copy["price_per_person"] = flight["price"]
            result["flights"].append(flight_copy)
    
    return json.dumps(result)

@tool
def get_flight_details(flight_number: str) -> str:
    """Get detailed information about a specific flight.
    
    Args:
        flight_number: Flight number (e.g., 'AF007', 'QR701')
    
    Returns:
        Detailed flight information including baggage, amenities, etc.
    """
    details = {
        "flight_number": flight_number,
        "aircraft": "Boeing 787 Dreamliner",
        "baggage": {
            "checked": "2 bags (23kg each)",
            "carry_on": "1 bag (10kg) + 1 personal item"
        },
        "amenities": [
            "In-flight entertainment",
            "WiFi available ($)",
            "Complimentary meals",
            "USB charging ports"
        ],
        "seat_options": {
            "economy": "Available",
            "premium_economy": "Available (+$200)",
            "business": "Available (+$1500)"
        }
    }
    
    return json.dumps(details)

