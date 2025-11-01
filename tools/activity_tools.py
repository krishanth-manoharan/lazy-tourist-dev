"""Activity and attraction research tools with mocked data"""
from langchain_core.tools import tool
from typing import Dict, List
import json

# Mock activities by destination
MOCK_ACTIVITIES = {
    "PARIS": [
        {
            "name": "Eiffel Tower Skip-the-Line Tour",
            "category": "Landmark",
            "duration": "2 hours",
            "price": 45,
            "rating": 4.8,
            "reviews": 12453,
            "description": "Skip the lines and enjoy breathtaking views from the iconic Eiffel Tower",
            "best_time": "Morning or sunset",
            "booking_link": "https://example.com/eiffel"
        },
        {
            "name": "Louvre Museum Guided Tour",
            "category": "Museum",
            "duration": "3 hours",
            "price": 65,
            "rating": 4.9,
            "reviews": 8932,
            "description": "Expert-led tour of the world's largest art museum",
            "best_time": "Morning to avoid crowds",
            "booking_link": "https://example.com/louvre"
        },
        {
            "name": "Seine River Dinner Cruise",
            "category": "Food & Dining",
            "duration": "2.5 hours",
            "price": 85,
            "rating": 4.7,
            "reviews": 5621,
            "description": "Romantic dinner cruise along the Seine with live music",
            "best_time": "Evening",
            "booking_link": "https://example.com/seine-cruise"
        },
        {
            "name": "Versailles Palace Day Trip",
            "category": "Historical",
            "duration": "6 hours",
            "price": 120,
            "rating": 4.8,
            "reviews": 7234,
            "description": "Full day tour of the magnificent Palace of Versailles and gardens",
            "best_time": "Full day, Tuesday-Sunday",
            "booking_link": "https://example.com/versailles"
        },
        {
            "name": "Montmartre Food Walking Tour",
            "category": "Food & Culture",
            "duration": "3 hours",
            "price": 75,
            "rating": 4.9,
            "reviews": 3421,
            "description": "Taste authentic French cuisine while exploring charming Montmartre",
            "best_time": "Afternoon",
            "booking_link": "https://example.com/montmartre-food"
        }
    ],
    "BALI": [
        {
            "name": "Tegalalang Rice Terrace Tour",
            "category": "Nature",
            "duration": "4 hours",
            "price": 35,
            "rating": 4.7,
            "reviews": 4521,
            "description": "Visit the stunning rice terraces and traditional villages",
            "best_time": "Morning",
            "booking_link": "https://example.com/rice-terrace"
        },
        {
            "name": "Balinese Spa & Massage Package",
            "category": "Wellness",
            "duration": "2 hours",
            "price": 50,
            "rating": 4.9,
            "reviews": 6234,
            "description": "Traditional Balinese massage and spa treatments",
            "best_time": "Afternoon",
            "booking_link": "https://example.com/spa"
        },
        {
            "name": "Tanah Lot Sunset Tour",
            "category": "Temple & Culture",
            "duration": "3 hours",
            "price": 40,
            "rating": 4.8,
            "reviews": 5892,
            "description": "Visit the iconic sea temple and watch the sunset",
            "best_time": "Late afternoon/sunset",
            "booking_link": "https://example.com/tanah-lot"
        },
        {
            "name": "Surfing Lesson in Canggu",
            "category": "Adventure",
            "duration": "2 hours",
            "price": 45,
            "rating": 4.7,
            "reviews": 2341,
            "description": "Learn to surf with experienced instructors",
            "best_time": "Morning",
            "booking_link": "https://example.com/surf"
        },
        {
            "name": "Ubud Monkey Forest & Waterfall",
            "category": "Nature",
            "duration": "5 hours",
            "price": 55,
            "rating": 4.6,
            "reviews": 3892,
            "description": "Explore the sacred monkey forest and hidden waterfalls",
            "best_time": "Morning",
            "booking_link": "https://example.com/monkey-forest"
        }
    ],
    "TOKYO": [
        {
            "name": "Tsukiji Fish Market & Sushi Breakfast",
            "category": "Food & Culture",
            "duration": "3 hours",
            "price": 80,
            "rating": 4.9,
            "reviews": 4521,
            "description": "Early morning fish market tour with fresh sushi breakfast",
            "best_time": "Early morning (5-8 AM)",
            "booking_link": "https://example.com/tsukiji"
        },
        {
            "name": "TeamLab Borderless Digital Art Museum",
            "category": "Art & Technology",
            "duration": "2 hours",
            "price": 35,
            "rating": 4.8,
            "reviews": 8234,
            "description": "Immersive digital art experience",
            "best_time": "Afternoon or evening",
            "booking_link": "https://example.com/teamlab"
        },
        {
            "name": "Mt. Fuji Day Trip",
            "category": "Nature",
            "duration": "10 hours",
            "price": 150,
            "rating": 4.7,
            "reviews": 5621,
            "description": "Full day tour to iconic Mt. Fuji and surrounding lakes",
            "best_time": "Full day, best in clear weather",
            "booking_link": "https://example.com/fuji"
        }
    ],
    "DEFAULT": [
        {
            "name": "City Walking Tour",
            "category": "Culture",
            "duration": "3 hours",
            "price": 30,
            "rating": 4.5,
            "reviews": 1000,
            "description": "Explore the city's main attractions with a local guide",
            "best_time": "Morning or afternoon",
            "booking_link": "https://example.com/city-tour"
        },
        {
            "name": "Local Food Experience",
            "category": "Food",
            "duration": "2 hours",
            "price": 50,
            "rating": 4.6,
            "reviews": 800,
            "description": "Taste authentic local cuisine",
            "best_time": "Evening",
            "booking_link": "https://example.com/food"
        }
    ]
}

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
    
    # Find matching activities - try partial matching
    activities = None
    for key in MOCK_ACTIVITIES.keys():
        if key == "DEFAULT":
            continue
        if key in dest_key or dest_key in key:
            activities = MOCK_ACTIVITIES[key]
            break
    
    # Use default if no match
    if not activities:
        activities = MOCK_ACTIVITIES["DEFAULT"]
    
    # Filter by price
    filtered_activities = [a for a in activities if a["price"] <= max_price]
    
    # Filter by interests if provided
    if interests:
        interest_keywords = interests.lower().split()
        interest_filtered = []
        for activity in filtered_activities:
            activity_text = (activity["name"] + " " + activity["category"] + " " + 
                           activity["description"]).lower()
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
    
    # Mock destination information
    dest_info = {
        "PARIS": {
            "best_time_to_visit": "April-June and September-October for pleasant weather and fewer crowds",
            "weather": "Temperate. Summers (18-25°C), Winters (3-8°C)",
            "visa_requirements": {
                "US_citizens": "No visa needed for stays up to 90 days",
                "UK_citizens": "No visa needed for stays up to 90 days",
                "general": "Schengen visa required for most non-EU nationals"
            },
            "currency": "Euro (EUR)",
            "language": "French (English widely spoken in tourist areas)",
            "safety_tips": [
                "Watch for pickpockets in tourist areas and metro",
                "Keep belongings secure in crowded places",
                "Paris is generally safe, but stay alert"
            ],
            "local_tips": [
                "Learn basic French phrases - locals appreciate the effort",
                "Restaurants typically serve lunch 12-2pm and dinner 7:30-10pm",
                "Buy museum passes to skip lines at major attractions",
                "Metro is the fastest way to get around"
            ],
            "emergency_numbers": "Police: 17, Ambulance: 15, Fire: 18"
        },
        "BALI": {
            "best_time_to_visit": "April-October (dry season) for best beach weather",
            "weather": "Tropical. Dry season (Apr-Oct), Wet season (Nov-Mar), 26-30°C year-round",
            "visa_requirements": {
                "US_citizens": "Visa on arrival (30 days) or e-visa available",
                "general": "Most nationalities can get visa on arrival for tourism"
            },
            "currency": "Indonesian Rupiah (IDR)",
            "language": "Indonesian and Balinese (English widely spoken in tourist areas)",
            "safety_tips": [
                "Be cautious when renting scooters - roads can be dangerous",
                "Drink bottled water only",
                "Be aware of your belongings in crowded areas",
                "Check surf conditions before swimming"
            ],
            "local_tips": [
                "Dress modestly when visiting temples",
                "Bargain at markets but not in established shops",
                "Tip is not mandatory but appreciated (10%)",
                "Be respectful during religious ceremonies"
            ],
            "emergency_numbers": "Police: 110, Ambulance: 118, Fire: 113"
        },
        "TOKYO": {
            "best_time_to_visit": "March-May (spring/cherry blossoms) or October-November (fall colors)",
            "weather": "Four distinct seasons. Spring/Fall: 15-20°C, Summer: hot & humid, Winter: cold",
            "visa_requirements": {
                "US_citizens": "No visa needed for stays up to 90 days",
                "general": "Many nationalities have visa-free access for tourism"
            },
            "currency": "Japanese Yen (JPY)",
            "language": "Japanese (English less common, especially outside tourist areas)",
            "safety_tips": [
                "Japan is very safe with low crime rates",
                "Be prepared for earthquakes - familiarize yourself with safety procedures",
                "Keep your belongings with you, but lost items are often returned"
            ],
            "local_tips": [
                "Get a Suica/Pasmo card for convenient train travel",
                "Tipping is not customary and may be refused",
                "Remove shoes when entering homes and some traditional restaurants",
                "Download a translation app - very helpful",
                "Many places are cash-only, carry yen"
            ],
            "emergency_numbers": "Police: 110, Ambulance/Fire: 119"
        }
    }
    
    dest_key = destination.upper()
    
    # Try to match destination
    info = None
    for key in dest_info.keys():
        if key in dest_key or dest_key in key:
            info = dest_info[key]
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
    
    return json.dumps(info)

