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
    
    # Get conversation history to maintain context
    conversation_history = state.get("conversation_history", [])
    
    # Build full query from conversation history
    # The initial query is already in conversation_history, so just use that
    full_query = "\n".join(conversation_history) if conversation_history else state.get("user_query", "")
    
    system_prompt = """You are an expert at extracting structured travel information from natural language.

    Extract the following information from the user's travel query and conversation history:
    - origin: departure city/airport
    - destination: arrival city/country
    - departure_date: when they want to leave (format: YYYY-MM-DD) [OPTIONAL - will default to 60 days from now]
    - return_date: when they want to return (format: YYYY-MM-DD) [OPTIONAL - will be calculated]
    - duration_days: number of days for the trip
    - num_adults: number of adult travelers
    - num_children: number of children [OPTIONAL - defaults to 0]
    - budget: total budget in USD
    - interests: list of interests (e.g., food, history, adventure, culture, beach, shopping) [OPTIONAL - defaults to general sightseeing]
    - min_hotel_stars: minimum hotel star rating [OPTIONAL - defaults to 3]

    Return a JSON object with two keys:
    {
        "extracted": {...},  // fields that were explicitly mentioned
        "missing": [...]     // list of ONLY critical fields that are missing
    }

    CRITICAL fields that MUST be provided: origin, destination, duration_days (or both departure_date and return_date), num_adults, budget
    OPTIONAL fields (do NOT include in missing): num_children, interests, min_hotel_stars, departure_date (if duration provided), return_date (if duration provided)

    If any CRITICAL field is missing, include it in the "missing" array.
    Do NOT include optional fields in the "missing" array - they have defaults.

    Return ONLY a valid JSON object. No other text."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Extract travel preferences from: {full_query}")
    ]
    
    response = model.invoke(messages)
    
    try:
        # Parse the JSON response
        result = json.loads(response.content)
        extracted = result.get("extracted", {})
        missing = result.get("missing", [])
        
        # Check if critical information is missing
        if missing:
            print(f"\n❓ Missing critical information: {', '.join(missing)}")
            
            # Use LLM to generate a natural conversational prompt
            ask_prompt = f"""You are a friendly travel agent. The user wants to plan a trip but is missing some information.

            Already provided: {json.dumps(extracted, indent=2)}
            Missing critical information: {', '.join(missing)}

            Generate a friendly, conversational message asking for the missing information. Be specific and helpful.
            Keep it concise and natural. Ask for all missing items in one message.

            Return ONLY the message text, no JSON."""
            
            ask_messages = [
                SystemMessage(content=ask_prompt),
                HumanMessage(content="Generate the message to ask for missing info")
            ]
            
            ask_response = model.invoke(ask_messages)
            feedback_message = ask_response.content.strip()
            
            print(f"\n💬 {feedback_message}")
            
            # Store partial extraction and mark that we need user input
            state["preferences"] = extracted
            state["needs_user_input"] = True
            state["feedback_message"] = feedback_message
            state["next_step"] = "collect_more_info"
            
            return state
        
        # All critical information is present - proceed with planning
        print(f"\n✅ All required information collected!")
        
        # Build preferences with defaults for optional fields
        preferences = {
            # Critical fields
            "origin": extracted.get("origin"),
            "destination": extracted.get("destination"),
            "num_adults": extracted.get("num_adults"),
            "budget": extracted.get("budget"),
            
            # Optional fields with defaults
            "num_children": extracted.get("num_children", 0),  # Default: 0 children
            "interests": extracted.get("interests") or ["sightseeing"],  # Default: general sightseeing
            "min_hotel_stars": extracted.get("min_hotel_stars", 3)  # Default: 3-star hotels
        }
        
        # Calculate dates with smart defaults
        # Departure date: default to 60 days from now if not provided
        if "departure_date" not in extracted or not extracted.get("departure_date"):
            departure = datetime.now() + timedelta(days=60)
            preferences["departure_date"] = departure.strftime("%Y-%m-%d")
        else:
            preferences["departure_date"] = extracted["departure_date"]
        
        # Handle duration and return date calculation
        if "duration_days" in extracted and extracted.get("duration_days"):
            preferences["duration_days"] = extracted["duration_days"]
            # Calculate return date from departure + duration
            if "return_date" not in extracted or not extracted.get("return_date"):
                dep_date = datetime.strptime(preferences["departure_date"], "%Y-%m-%d")
                ret_date = dep_date + timedelta(days=preferences["duration_days"])
                preferences["return_date"] = ret_date.strftime("%Y-%m-%d")
            else:
                preferences["return_date"] = extracted["return_date"]
        elif "return_date" in extracted and extracted.get("return_date"):
            # Calculate duration from dates
            preferences["return_date"] = extracted["return_date"]
            dep_date = datetime.strptime(preferences["departure_date"], "%Y-%m-%d")
            ret_date = datetime.strptime(preferences["return_date"], "%Y-%m-%d")
            preferences["duration_days"] = (ret_date - dep_date).days
        else:
            # Fallback: use default 5-day duration
            preferences["duration_days"] = 5
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
        state["needs_user_input"] = False
        state["next_step"] = "research_destination"
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing LLM response: {e}")
        print(f"Response content: {response.content}")
        
        # Mark that we need user input and ask them to rephrase
        state["needs_user_input"] = True
        state["feedback_message"] = "I'm having trouble understanding your request. Could you please tell me where you'd like to go, how many days, how many people, and your budget?"
        state["next_step"] = "collect_more_info"
    
    return state

