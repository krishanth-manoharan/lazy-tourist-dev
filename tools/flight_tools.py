"""Flight search tools with mocked API responses"""
from langchain_core.tools import tool
from typing import Dict, List
import random
import json
from datetime import datetime, timedelta

# Mock flight data
MOCK_FLIGHTS = {
    "NYC-PARIS": [
        {
            "airline": "Air France",
            "flight_number": "AF007",
            "departure": "JFK",
            "arrival": "CDG",
            "duration": "7h 30m",
            "price": 650,
            "stops": 0,
            "departure_time": "22:30",
            "arrival_time": "12:00+1"
        },
        {
            "airline": "Delta",
            "flight_number": "DL264",
            "departure": "JFK",
            "arrival": "CDG",
            "duration": "8h 15m",
            "price": 580,
            "stops": 0,
            "departure_time": "18:15",
            "arrival_time": "07:30+1"
        },
        {
            "airline": "United",
            "flight_number": "UA57",
            "departure": "EWR",
            "arrival": "CDG",
            "duration": "7h 45m",
            "price": 720,
            "stops": 0,
            "departure_time": "20:00",
            "arrival_time": "09:45+1"
        }
    ],
    "NYC-BALI": [
        {
            "airline": "Qatar Airways",
            "flight_number": "QR701",
            "departure": "JFK",
            "arrival": "DPS",
            "duration": "22h 30m",
            "price": 1150,
            "stops": 1,
            "layover": "DOH - 3h 20m",
            "departure_time": "23:00",
            "arrival_time": "06:30+2"
        },
        {
            "airline": "Singapore Airlines",
            "flight_number": "SQ21",
            "departure": "JFK",
            "arrival": "DPS",
            "duration": "24h 15m",
            "price": 1280,
            "stops": 1,
            "layover": "SIN - 4h 10m",
            "departure_time": "01:30",
            "arrival_time": "10:45+2"
        },
        {
            "airline": "Korean Air",
            "flight_number": "KE086",
            "departure": "JFK",
            "arrival": "DPS",
            "duration": "23h 45m",
            "price": 1050,
            "stops": 1,
            "layover": "ICN - 2h 50m",
            "departure_time": "13:45",
            "arrival_time": "22:30+2"
        }
    ],
    "NYC-TOKYO": [
        {
            "airline": "ANA",
            "flight_number": "NH9",
            "departure": "JFK",
            "arrival": "NRT",
            "duration": "14h 10m",
            "price": 950,
            "stops": 0,
            "departure_time": "13:10",
            "arrival_time": "16:20+1"
        },
        {
            "airline": "JAL",
            "flight_number": "JL006",
            "departure": "JFK",
            "arrival": "HND",
            "duration": "13h 50m",
            "price": 1020,
            "stops": 0,
            "departure_time": "11:50",
            "arrival_time": "14:40+1"
        }
    ],
    "DEFAULT": [
        {
            "airline": "International Airways",
            "flight_number": "IA123",
            "departure": "ORIGIN",
            "arrival": "DEST",
            "duration": "8h 00m",
            "price": 800,
            "stops": 0,
            "departure_time": "10:00",
            "arrival_time": "18:00"
        },
        {
            "airline": "Global Airlines",
            "flight_number": "GA456",
            "departure": "ORIGIN",
            "arrival": "DEST",
            "duration": "9h 30m",
            "price": 650,
            "stops": 1,
            "layover": "HUB - 2h",
            "departure_time": "14:00",
            "arrival_time": "23:30"
        }
    ]
}

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

