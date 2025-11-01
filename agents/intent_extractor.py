"""Intent extraction agent - parses user query to extract travel preferences"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from agents.state import TravelState
import json
import re
from datetime import datetime, timedelta

def extract_intent(state: TravelState) -> TravelState:
    """Extract travel preferences from user query using LLM"""
    print("\n" + "="*60)
    print("🧠 INTENT EXTRACTOR - Analyzing user requirements...")
    print("="*60)
    
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """You are an expert at extracting structured travel information from natural language.

Extract the following information from the user's travel query:
- origin: departure city/airport
- destination: arrival city/country
- departure_date: when they want to leave (format: YYYY-MM-DD)
- return_date: when they want to return (format: YYYY-MM-DD)
- duration_days: number of days for the trip
- num_adults: number of adult travelers
- num_children: number of children
- budget: total budget in USD
- interests: list of interests (e.g., food, history, adventure, culture, beach, shopping)
- min_hotel_stars: minimum hotel star rating (default: 3)

Return a JSON object with two keys:
{
    "extracted": {...},  // fields that were explicitly mentioned
    "missing": [...]     // list of critical fields that are missing
}

Critical fields that MUST be provided: origin, destination, duration_days (or dates), num_adults, budget
If any critical field is missing, include it in the "missing" array.

Return ONLY a valid JSON object. No other text."""

    user_message = state.get("user_query", "")
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Extract travel preferences from: {user_message}")
    ]
    
    response = model.invoke(messages)
    
    try:
        # Parse the JSON response
        result = json.loads(response.content)
        extracted = result.get("extracted", {})
        missing = result.get("missing", [])
        
        # Check if critical information is missing
        if missing:
            print(f"\n❓ I need some more information to plan your trip:")
            
            # Ask for missing information
            for field in missing:
                if field == "origin":
                    origin = input("\n🛫 Where are you traveling from? ").strip()
                    if origin:
                        extracted["origin"] = origin
                    else:
                        extracted["origin"] = "NYC"
                
                elif field == "destination":
                    destination = input("\n📍 Where would you like to go? ").strip()
                    if destination:
                        extracted["destination"] = destination
                
                elif field == "duration_days":
                    duration = input("\n📅 How many days is your trip? ").strip()
                    if duration.isdigit():
                        extracted["duration_days"] = int(duration)
                
                elif field == "num_adults":
                    adults = input("\n👥 How many adults are traveling? ").strip()
                    if adults.isdigit():
                        extracted["num_adults"] = int(adults)
                    else:
                        extracted["num_adults"] = 2
                
                elif field == "budget":
                    budget = input("\n💰 What's your total budget (in USD)? $").strip()
                    if budget.isdigit():
                        extracted["budget"] = int(budget)
        
        # Set defaults for optional fields
        preferences = {
            "origin": extracted.get("origin") or "NYC",
            "destination": extracted.get("destination") or "Paris",
            "num_adults": extracted.get("num_adults") or 2,
            "num_children": extracted.get("num_children") or 0,
            "budget": extracted.get("budget") or 3000,
            "interests": extracted.get("interests") or ["sightseeing"],
            "min_hotel_stars": extracted.get("min_hotel_stars") or 3
        }
        
        # Calculate dates if needed
        if "departure_date" not in extracted or not extracted.get("departure_date"):
            departure = datetime.now() + timedelta(days=60)
            preferences["departure_date"] = departure.strftime("%Y-%m-%d")
        else:
            preferences["departure_date"] = extracted["departure_date"]
        
        # Handle duration and return date
        if "duration_days" in extracted and extracted.get("duration_days"):
            preferences["duration_days"] = extracted["duration_days"]
            if "return_date" not in extracted or not extracted.get("return_date"):
                dep_date = datetime.strptime(preferences["departure_date"], "%Y-%m-%d")
                ret_date = dep_date + timedelta(days=preferences["duration_days"])
                preferences["return_date"] = ret_date.strftime("%Y-%m-%d")
            else:
                preferences["return_date"] = extracted["return_date"]
        elif "return_date" in extracted and extracted.get("return_date"):
            preferences["return_date"] = extracted["return_date"]
            dep_date = datetime.strptime(preferences["departure_date"], "%Y-%m-%d")
            ret_date = datetime.strptime(preferences["return_date"], "%Y-%m-%d")
            preferences["duration_days"] = (ret_date - dep_date).days
        else:
            # No duration or return date provided, ask for duration
            if "duration_days" not in preferences:
                # Already asked in missing fields above, but double-check
                preferences["duration_days"] = 5  # default
            
            dep_date = datetime.strptime(preferences["departure_date"], "%Y-%m-%d")
            ret_date = dep_date + timedelta(days=preferences["duration_days"])
            preferences["return_date"] = ret_date.strftime("%Y-%m-%d")
        
        # Calculate total passengers
        preferences["total_passengers"] = preferences["num_adults"] + preferences["num_children"]
        
        print(f"\n✅ Got it! Planning your trip:")
        print(f"   📍 Route: {preferences['origin']} → {preferences['destination']}")
        print(f"   📅 Dates: {preferences['departure_date']} to {preferences.get('return_date', 'TBD')}")
        print(f"   👥 Travelers: {preferences['total_passengers']} ({preferences['num_adults']} adults, {preferences['num_children']} children)")
        print(f"   💰 Budget: ${preferences['budget']}")
        print(f"   🎯 Interests: {', '.join(preferences['interests'])}")
        
        state["preferences"] = preferences
        state["next_step"] = "research_destination"
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing response: {e}")
        # Ask for essential information
        print("\nLet me ask you a few questions to plan your trip:")
        
        destination = input("\n📍 Where would you like to go? ").strip() or "Paris"
        duration = input("📅 How many days? ").strip()
        duration_days = int(duration) if duration.isdigit() else 5
        adults = input("👥 How many adults? ").strip()
        num_adults = int(adults) if adults.isdigit() else 2
        budget = input("💰 Total budget (USD)? $").strip()
        budget_amount = int(budget) if budget.isdigit() else 3000
        
        departure = datetime.now() + timedelta(days=60)
        ret_date = departure + timedelta(days=duration_days)
        
        state["preferences"] = {
            "origin": "NYC",
            "destination": destination,
            "departure_date": departure.strftime("%Y-%m-%d"),
            "return_date": ret_date.strftime("%Y-%m-%d"),
            "duration_days": duration_days,
            "num_adults": num_adults,
            "num_children": 0,
            "total_passengers": num_adults,
            "budget": budget_amount,
            "interests": ["sightseeing", "food"],
            "min_hotel_stars": 3
        }
        state["next_step"] = "research_destination"
    
    return state

