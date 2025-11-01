"""Search agents for flights, hotels, and activities"""
from agents.state import TravelState
from tools.flight_tools import search_flights, search_return_flights
from tools.hotel_tools import search_hotels
from tools.activity_tools import search_activities, get_destination_info
import json

def flight_search_agent(state: TravelState) -> TravelState:
    """Search for flight options - both outbound and return"""
    print("\n" + "="*60)
    print("✈️  FLIGHT SEARCH AGENT - Finding best flights...")
    print("="*60)
    
    prefs = state["preferences"]
    
    # Allocate 40% of budget to flights (both ways combined)
    max_flight_price = int(prefs["budget"] * 0.4 / 2)  # Divide by 2 for outbound + return
    
    # Search for outbound flights
    result = search_flights.invoke({
        "origin": prefs["origin"],
        "destination": prefs["destination"],
        "departure_date": prefs["departure_date"],
        "passengers": prefs["total_passengers"],
        "max_price": max_flight_price
    })
    
    # Parse outbound flight results
    try:
        flight_data = json.loads(result)
        flights = flight_data.get("flights", [])
        message = flight_data.get("message", "")
        state["flights"] = flights
        
        if message:
            print(f"\n⚠️  {message}")
            print("   💡 Tip: Consider increasing your budget or adjusting your search criteria.")
        elif flights:
            print(f"\n✅ Found {len(flights)} outbound flight options:")
            for i, flight in enumerate(flights, 1):
                stops_text = "Direct" if flight.get("stops", 0) == 0 else f"{flight['stops']} stop(s)"
                print(f"   {i}. {flight.get('airline', 'Unknown')} {flight.get('flight_number', '')} - "
                      f"${flight.get('total_price', 0)} ({stops_text}) - {flight.get('duration', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error parsing outbound flight results: {e}")
        state["flights"] = []
    
    # Search for return flights
    return_result = search_return_flights.invoke({
        "origin": prefs["origin"],
        "destination": prefs["destination"],
        "return_date": prefs["return_date"],
        "passengers": prefs["total_passengers"],
        "max_price": max_flight_price
    })
    
    # Parse return flight results
    try:
        return_flight_data = json.loads(return_result)
        return_flights = return_flight_data.get("flights", [])
        return_message = return_flight_data.get("message", "")
        state["return_flights"] = return_flights
        
        if return_message:
            print(f"\n⚠️  {return_message}")
            print("   💡 Tip: Consider increasing your budget or adjusting your search criteria.")
        elif return_flights:
            print(f"\n✅ Found {len(return_flights)} return flight options:")
            for i, flight in enumerate(return_flights, 1):
                stops_text = "Direct" if flight.get("stops", 0) == 0 else f"{flight['stops']} stop(s)"
                print(f"   {i}. {flight.get('airline', 'Unknown')} {flight.get('flight_number', '')} - "
                      f"${flight.get('total_price', 0)} ({stops_text}) - {flight.get('duration', 'N/A')}")
        
        state["next_step"] = "search_hotels"
        
    except Exception as e:
        print(f"❌ Error parsing return flight results: {e}")
        state["return_flights"] = []
        state["next_step"] = "search_hotels"
    
    return state

def hotel_search_agent(state: TravelState) -> TravelState:
    """Search for hotel options"""
    print("\n" + "="*60)
    print("🏨 HOTEL SEARCH AGENT - Finding accommodations...")
    print("="*60)
    
    prefs = state["preferences"]
    
    # Calculate max hotel budget (30% of total budget, divided by nights)
    hotel_budget_total = prefs["budget"] * 0.3
    nights = prefs.get("duration_days", 5) - 1  # Assuming last day is return
    max_per_night = int(hotel_budget_total / nights) if nights > 0 else 200
    
    result = search_hotels.invoke({
        "destination": prefs["destination"],
        "check_in": prefs["departure_date"],
        "check_out": prefs.get("return_date", prefs["departure_date"]),
        "guests": prefs["total_passengers"],
        "min_stars": prefs.get("min_hotel_stars", 3),
        "max_price_per_night": max_per_night
    })
    
    # Parse result
    try:
        hotel_data = json.loads(result)
        hotels = hotel_data.get("hotels", [])
        message = hotel_data.get("message", "")
        state["hotels"] = hotels
        
        if message:
            print(f"\n⚠️  {message}")
            print("   💡 Tip: Consider increasing your budget or adjusting your hotel preferences.")
        elif hotels:
            print(f"\n✅ Found {len(hotels)} hotel options:")
            for i, hotel in enumerate(hotels, 1):
                print(f"   {i}. {hotel.get('name', 'Unknown')} - "
                      f"{hotel.get('stars', 0)}⭐ - "
                      f"${hotel.get('price_per_night', 0)}/night - "
                      f"${hotel.get('total_price', 0)} total ({hotel.get('nights', 0)} nights)")
        
        state["next_step"] = "search_activities"
        
    except Exception as e:
        print(f"❌ Error parsing hotel results: {e}")
        state["hotels"] = []
        state["next_step"] = "search_activities"
    
    return state

def activity_research_agent(state: TravelState) -> TravelState:
    """Research activities and attractions"""
    print("\n" + "="*60)
    print("🎯 ACTIVITY RESEARCH AGENT - Finding experiences...")
    print("="*60)
    
    prefs = state["preferences"]
    
    # Get destination info first
    dest_info_result = get_destination_info.invoke({"destination": prefs["destination"]})
    try:
        state["destination_info"] = json.loads(dest_info_result)
        print(f"\n📍 Destination Info Retrieved:")
        dest_info = state["destination_info"]
        print(f"   Best time to visit: {dest_info.get('best_time_to_visit', 'N/A')}")
        print(f"   Currency: {dest_info.get('currency', 'N/A')}")
    except:
        state["destination_info"] = {}
    
    # Search for activities based on interests
    interests_str = " ".join(prefs.get("interests", []))
    activity_budget = int(prefs["budget"] * 0.2)  # 20% for activities
    
    result = search_activities.invoke({
        "destination": prefs["destination"],
        "interests": interests_str,
        "max_price": 200
    })
    
    # Parse result
    try:
        activity_data = json.loads(result)
        activities = activity_data.get("activities", [])
        state["activities"] = activities
        
        print(f"\n✅ Found {len(activities)} activities:")
        for i, activity in enumerate(activities, 1):
            print(f"   {i}. {activity.get('name', 'Unknown')} - "
                  f"${activity.get('price', 0)} - "
                  f"{activity.get('duration', 'N/A')} - "
                  f"⭐{activity.get('rating', 0)}")
        
        state["next_step"] = "compile_itinerary"
        
    except Exception as e:
        print(f"❌ Error parsing activity results: {e}")
        state["activities"] = []
        state["next_step"] = "compile_itinerary"
    
    return state

def destination_research_agent(state: TravelState) -> TravelState:
    """Research destination information"""
    print("\n" + "="*60)
    print("🌍 DESTINATION RESEARCH AGENT - Gathering intel...")
    print("="*60)
    
    prefs = state["preferences"]
    
    # Get comprehensive destination info
    result = get_destination_info.invoke({"destination": prefs["destination"]})
    
    try:
        dest_info = json.loads(result)
        state["destination_info"] = dest_info
        
        print(f"\n✅ Destination Research Complete:")
        print(f"   🌤️  Best Time: {dest_info.get('best_time_to_visit', 'N/A')}")
        print(f"   💱 Currency: {dest_info.get('currency', 'N/A')}")
        print(f"   🗣️  Language: {dest_info.get('language', 'N/A')}")
        
        if "visa_requirements" in dest_info:
            visa = dest_info["visa_requirements"]
            if isinstance(visa, dict) and "US_citizens" in visa:
                print(f"   🛂 Visa (US): {visa['US_citizens']}")
        
        state["next_step"] = "search_flights"
        
    except Exception as e:
        print(f"❌ Error parsing destination info: {e}")
        state["destination_info"] = {}
        state["next_step"] = "search_flights"
    
    return state

