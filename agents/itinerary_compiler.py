"""Itinerary compilation agent - creates day-by-day plans"""
from agents.state import TravelState, DayPlan, BudgetBreakdown
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime, timedelta
import json

def compile_itinerary(state: TravelState) -> TravelState:
    """Compile a complete day-by-day itinerary"""
    print("\n" + "="*60)
    print("📋 ITINERARY COMPILER - Creating your perfect trip...")
    print("="*60)
    
    prefs = state["preferences"]
    flights = state.get("flights", [])
    return_flights = state.get("return_flights", [])
    hotels = state.get("hotels", [])
    activities = state.get("activities", [])
    
    # Select best options (for now, select first/cheapest)
    selected_flight = flights[0] if flights else None
    selected_return_flight = return_flights[0] if return_flights else None
    selected_hotel = hotels[0] if hotels else None
    
    if selected_flight:
        state["selected_flight"] = selected_flight
        print(f"\n✈️  Selected Outbound Flight: {selected_flight.get('airline')} {selected_flight.get('flight_number')} - ${selected_flight.get('total_price')}")
    
    if selected_return_flight:
        state["selected_return_flight"] = selected_return_flight
        print(f"✈️  Selected Return Flight: {selected_return_flight.get('airline')} {selected_return_flight.get('flight_number')} - ${selected_return_flight.get('total_price')}")
    
    if selected_hotel:
        state["selected_hotel"] = selected_hotel
        print(f"🏨 Selected Hotel: {selected_hotel.get('name')} - ${selected_hotel.get('total_price')} total")
    
    # Create daily itinerary
    duration = prefs.get("duration_days", 5)
    daily_itinerary = []
    
    # Distribute activities across days (skip first and last day for travel)
    activity_days = max(1, duration - 2)
    activities_per_day = max(1, len(activities) // activity_days) if activity_days > 0 and len(activities) > 0 else 2
    
    print(f"\n📅 Planning {duration} days with {len(activities)} activities ({activities_per_day} per day)")
    
    start_date = datetime.strptime(prefs["departure_date"], "%Y-%m-%d")
    
    for day in range(1, duration + 1):
        current_date = start_date + timedelta(days=day - 1)
        day_plan = {
            "day": day,
            "date": current_date.strftime("%Y-%m-%d"),
            "activities": [],
            "estimated_cost": 0,
            "notes": ""
        }
        
        if day == 1:
            # Arrival day
            day_plan["notes"] = f"Arrival day - Flight arrives, check into {selected_hotel.get('name', 'hotel') if selected_hotel else 'hotel'}"
            day_plan["activities"] = [{
                "name": "Airport Transfer & Hotel Check-in",
                "duration": "2-3 hours",
                "price": 0,
                "description": "Arrive at destination and settle into accommodation"
            }]
        elif day == duration:
            # Departure day
            day_plan["notes"] = f"Departure day - Check out and head to airport"
            day_plan["activities"] = [{
                "name": "Hotel Check-out & Airport Transfer",
                "duration": "2-3 hours",
                "price": 0,
                "description": "Check out and depart for return flight"
            }]
        else:
            # Activity days
            start_idx = (day - 2) * activities_per_day
            end_idx = min(start_idx + activities_per_day, len(activities))
            day_activities = activities[start_idx:end_idx]
            
            for activity in day_activities:
                day_plan["activities"].append({
                    "name": activity.get("name", "Activity"),
                    "category": activity.get("category", ""),
                    "duration": activity.get("duration", ""),
                    "price": activity.get("price", 0),
                    "rating": activity.get("rating", 0),
                    "description": activity.get("description", ""),
                    "best_time": activity.get("best_time", "")
                })
                day_plan["estimated_cost"] += activity.get("price", 0)
            
            day_plan["notes"] = f"Exploration day - {len(day_activities)} activities planned"
        
        daily_itinerary.append(day_plan)
    
    state["daily_itinerary"] = daily_itinerary
    
    # Calculate budget
    outbound_flight_cost = selected_flight.get("total_price", 0) if selected_flight else 0
    return_flight_cost = selected_return_flight.get("total_price", 0) if selected_return_flight else 0
    total_flight_cost = outbound_flight_cost + return_flight_cost
    hotel_cost = selected_hotel.get("total_price", 0) if selected_hotel else 0
    activity_cost = sum(day.get("estimated_cost", 0) for day in daily_itinerary)
    
    # Estimate meals and transportation
    meals_per_day = 50 * prefs.get("total_passengers", 2)
    meals_total = meals_per_day * duration
    transportation_total = 100  # Local transport estimate
    misc_total = 200  # Miscellaneous
    
    total_cost = total_flight_cost + hotel_cost + activity_cost + meals_total + transportation_total + misc_total
    
    budget_breakdown = {
        "flights": total_flight_cost,
        "accommodation": hotel_cost,
        "activities": activity_cost,
        "meals": meals_total,
        "transportation": transportation_total,
        "miscellaneous": misc_total,
        "total": total_cost,
        "remaining": prefs.get("budget", 3000) - total_cost
    }
    
    state["budget"] = budget_breakdown
    
    print(f"\n💰 Budget Breakdown:")
    print(f"   Flights (Round-trip): ${budget_breakdown['flights']}")
    print(f"     → Outbound: ${outbound_flight_cost}")
    print(f"     → Return: ${return_flight_cost}")
    print(f"   Accommodation: ${budget_breakdown['accommodation']}")
    print(f"   Activities: ${budget_breakdown['activities']}")
    print(f"   Meals: ${budget_breakdown['meals']}")
    print(f"   Transportation: ${budget_breakdown['transportation']}")
    print(f"   Miscellaneous: ${budget_breakdown['miscellaneous']}")
    print(f"   {'─'*40}")
    print(f"   TOTAL: ${budget_breakdown['total']} / ${prefs.get('budget', 3000)} budget")
    remaining = budget_breakdown['remaining']
    if remaining >= 0:
        print(f"   ✅ Under budget by ${remaining}")
    else:
        print(f"   ⚠️  Over budget by ${abs(remaining)}")
    
    state["next_step"] = "format_output"
    
    return state

def format_final_itinerary(state: TravelState) -> TravelState:
    """Format the final itinerary in a beautiful markdown format using LLM"""
    print("\n" + "="*60)
    print("📄 FORMATTER - Using AI to create beautiful itinerary document...")
    print("="*60)
    
    from tools.itinerary_tools import set_itinerary_content
    
    prefs = state["preferences"]
    selected_flight = state.get("selected_flight", {})
    selected_return_flight = state.get("selected_return_flight", {})
    selected_hotel = state.get("selected_hotel", {})
    daily_itinerary = state.get("daily_itinerary", [])
    budget = state.get("budget", {})
    dest_info = state.get("destination_info", {})
    
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    system_prompt = """You are an expert travel itinerary formatter. Your task is to create a beautiful, well-structured markdown document for a travel itinerary.

    Create a professional markdown document with the following structure:
    1. A compelling creative title
    2. Trip Overview section with key details
    3. Flight Details section (outbound and return)
    4. Accommodation section with hotel details
    5. Day-by-Day Itinerary with all activities for each day
    6. Budget Breakdown section with a table
    7. Destination Tips section (if available)
    8. A closing message

    Use appropriate emojis, formatting, and structure to make it visually appealing and easy to read.
    Use markdown tables, lists, bold text, and proper headings.
    Include all the information provided - don't omit any details.
    Make it engaging and travel-friendly.
    
    IMPORTANT - Image formatting:
    - If you include images (from image_url fields), always use HTML img tags with explicit width attribute
    - Format images as: <img src="URL" alt="description" width="80mm">
    - DO NOT use CSS style attributes like style="max-width: 80mm" - use the width attribute directly
    - This ensures images are properly sized for PDF generation and don't overflow the page"""
    
    # Build comprehensive user message with all itinerary data
    itinerary_data = {
        "preferences": prefs,
        "outbound_flight": selected_flight,
        "return_flight": selected_return_flight,
        "hotel": selected_hotel,
        "daily_itinerary": daily_itinerary,
        "budget": budget,
        "destination_info": dest_info
    }
    
    user_message = f"""Create a beautiful markdown itinerary document using the following travel data:

    TRIP PREFERENCES:
    - Destination: {prefs.get('destination', 'N/A')}
    - Dates: {prefs.get('departure_date', 'N/A')} to {prefs.get('return_date', 'N/A')}
    - Duration: {prefs.get('duration_days', 0)} days
    - Travelers: {prefs.get('num_adults', 0)} adults, {prefs.get('num_children', 0)} children
    - Budget: ${prefs.get('budget', 0)}
    - Interests: {', '.join(prefs.get('interests', []))}

    OUTBOUND FLIGHT:
    {json.dumps(selected_flight, indent=2) if selected_flight else "No outbound flight selected"}

    RETURN FLIGHT:
    {json.dumps(selected_return_flight, indent=2) if selected_return_flight else "No return flight selected"}

    ACCOMMODATION:
    {json.dumps(selected_hotel, indent=2) if selected_hotel else "No hotel selected"}

    DAILY ITINERARY:
    {json.dumps(daily_itinerary, indent=2) if daily_itinerary else "No daily itinerary"}

    BUDGET BREAKDOWN:
    {json.dumps(budget, indent=2) if budget else "No budget breakdown"}

    DESTINATION INFORMATION:
    {json.dumps(dest_info, indent=2) if dest_info else "No destination info available"}

    Generate a complete, well-formatted markdown document that includes all this information in an organized and visually appealing way. Use proper markdown syntax including:
    - Headers (#, ##, ###)
    - Bold text (**text**)
    - Lists (- item)
    - Tables (| column | column |)
    - No emojies
    - Horizontal rules (---)
    
    IMAGE FORMATTING RULES:
    - If hotel or activity data includes image_url fields, include the images in the appropriate sections
    - ALWAYS format images using HTML img tags with explicit width attribute: <img src="URL" alt="description" width="80mm">
    - DO NOT use CSS style attributes (style="max-width: 80mm") - the PDF library doesn't support them
    - Never use raw markdown image syntax ![alt](url) for images that need size control
    - Example: <img src="https://example.com/hotel.jpg" alt="Hotel view" width="80mm">
    - The width attribute directly controls image size in the PDF output

    Return ONLY the markdown content, no additional text or explanation."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    print("\n🤖 Generating markdown with AI...")
    response = model.invoke(messages)
    
    # Extract markdown from LLM response
    markdown = response.content.strip()
    
    # Clean up any code block markers if LLM wrapped it in them
    if markdown.startswith("```markdown"):
        markdown = markdown[11:].strip()
    elif markdown.startswith("```"):
        markdown = markdown[3:].strip()
    if markdown.endswith("```"):
        markdown = markdown[:-3].strip()
    
    state["final_itinerary"] = markdown
    
    # Store in global itinerary content for tools to access
    set_itinerary_content(markdown)
    
    print("\n✅ Markdown generated successfully!")
    
    # In conversational mode, go to feedback; otherwise complete
    if state.get("iteration_count", 0) == 0:
        state["next_step"] = "get_feedback"
        print("\n✅ Itinerary created! Getting your feedback...")
    else:
        state["next_step"] = "get_feedback"
        print("\n✅ Itinerary updated based on your feedback!")
    
    return state

