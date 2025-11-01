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
    """Format the final itinerary in a beautiful markdown format"""
    print("\n" + "="*60)
    print("📄 FORMATTER - Creating beautiful itinerary document...")
    print("="*60)
    
    from tools.itinerary_tools import set_itinerary_content
    
    prefs = state["preferences"]
    selected_flight = state.get("selected_flight", {})
    selected_return_flight = state.get("selected_return_flight", {})
    selected_hotel = state.get("selected_hotel", {})
    daily_itinerary = state.get("daily_itinerary", [])
    budget = state.get("budget", {})
    dest_info = state.get("destination_info", {})
    
    markdown = f"""# 🌍 Your Personalized Travel Itinerary
    ## {prefs.get('destination', 'Destination')} Adventure

    ---

    ## 📋 Trip Overview

    **Destination:** {prefs.get('destination', 'N/A')}  
    **Dates:** {prefs.get('departure_date', 'N/A')} to {prefs.get('return_date', 'N/A')}  
    **Duration:** {prefs.get('duration_days', 0)} days  
    **Travelers:** {prefs.get('num_adults', 0)} adults, {prefs.get('num_children', 0)} children  
    **Budget:** ${prefs.get('budget', 0)}

    ---

    ## ✈️ Flight Details

    **Outbound Flight:**  
    - **Airline:** {selected_flight.get('airline', 'N/A')} {selected_flight.get('flight_number', '')}  
    - **Route:** {selected_flight.get('departure', 'N/A')} → {selected_flight.get('arrival', 'N/A')}  
    - **Departure:** {selected_flight.get('departure_time', 'N/A')} on {prefs.get('departure_date', 'N/A')}  
    - **Arrival:** {selected_flight.get('arrival_time', 'N/A')}  
    - **Duration:** {selected_flight.get('duration', 'N/A')}  
    - **Stops:** {selected_flight.get('stops', 0)}  
    - **Price:** ${selected_flight.get('total_price', 0)} (${selected_flight.get('price_per_person', 0)}/person)

    **Return Flight:**  
    - **Airline:** {selected_return_flight.get('airline', 'N/A')} {selected_return_flight.get('flight_number', '')}  
    - **Route:** {selected_return_flight.get('departure', 'N/A')} → {selected_return_flight.get('arrival', 'N/A')}  
    - **Departure:** {selected_return_flight.get('departure_time', 'N/A')} on {prefs.get('return_date', 'N/A')}  
    - **Arrival:** {selected_return_flight.get('arrival_time', 'N/A')}  
    - **Duration:** {selected_return_flight.get('duration', 'N/A')}  
    - **Stops:** {selected_return_flight.get('stops', 0)}  
    - **Price:** ${selected_return_flight.get('total_price', 0)} (${selected_return_flight.get('price_per_person', 0)}/person)

    **Total Flight Cost:** ${selected_flight.get('total_price', 0) + selected_return_flight.get('total_price', 0)}

    ---

    ## 🏨 Accommodation

    **Hotel:** {selected_hotel.get('name', 'N/A')}  
    **Rating:** {selected_hotel.get('stars', 0)}⭐ ({selected_hotel.get('rating', 0)}/5.0 - {selected_hotel.get('reviews', 0)} reviews)  
    **Location:** {selected_hotel.get('location', 'N/A')} - {selected_hotel.get('distance_to_center', 'N/A')}  
    **Price:** ${selected_hotel.get('price_per_night', 0)}/night × {selected_hotel.get('nights', 0)} nights = ${selected_hotel.get('total_price', 0)}

    **Amenities:**  
    """
    
    for amenity in selected_hotel.get('amenities', []):
        markdown += f"- {amenity}\n"
    
    markdown += f"""
    ---

    ## 📅 Day-by-Day Itinerary

    """
    
    for day_plan in daily_itinerary:
        markdown += f"""### Day {day_plan['day']} - {day_plan['date']}
    *{day_plan['notes']}*

    """
        for activity in day_plan.get('activities', []):
            markdown += f"""**{activity.get('name', 'Activity')}**  
    """
            if activity.get('category'):
                markdown += f"- Category: {activity['category']}\n"
            if activity.get('duration'):
                markdown += f"- Duration: {activity['duration']}\n"
            if activity.get('price', 0) > 0:
                markdown += f"- Price: ${activity['price']}\n"
            if activity.get('rating'):
                markdown += f"- Rating: ⭐{activity['rating']}/5.0\n"
            if activity.get('description'):
                markdown += f"- {activity['description']}\n"
            if activity.get('best_time'):
                markdown += f"- Best time: {activity['best_time']}\n"
            markdown += "\n"
        
        if day_plan.get('estimated_cost', 0) > 0:
            markdown += f"**Estimated cost for day:** ${day_plan['estimated_cost']}\n"
        markdown += "\n---\n\n"
    
    markdown += f"""## 💰 Budget Breakdown

    | Category | Cost |
    |----------|------|
    | Flights | ${budget.get('flights', 0)} |
    | Accommodation | ${budget.get('accommodation', 0)} |
    | Activities | ${budget.get('activities', 0)} |
    | Meals (estimated) | ${budget.get('meals', 0)} |
    | Local Transportation | ${budget.get('transportation', 0)} |
    | Miscellaneous | ${budget.get('miscellaneous', 0)} |
    | **TOTAL** | **${budget.get('total', 0)}** |

    **Your Budget:** ${prefs.get('budget', 0)}  
    """
    
    remaining = budget.get('remaining', 0)
    if remaining >= 0:
        markdown += f"**Remaining:** ${remaining} ✅\n"
    else:
        markdown += f"**Over Budget:** ${abs(remaining)} ⚠️\n"
    
    # Add destination tips
    if dest_info:
        markdown += f"""
        ---

        ## 🌟 Destination Tips

        """
        if dest_info.get('best_time_to_visit'):
            markdown += f"**Best Time to Visit:** {dest_info['best_time_to_visit']}\n\n"
        
        if dest_info.get('currency'):
            markdown += f"**Currency:** {dest_info['currency']}\n\n"
        
        if dest_info.get('language'):
            markdown += f"**Language:** {dest_info['language']}\n\n"
        
        if dest_info.get('visa_requirements'):
            visa = dest_info['visa_requirements']
            markdown += "**Visa Requirements:**\n"
            if isinstance(visa, dict):
                for key, value in visa.items():
                    markdown += f"- {key}: {value}\n"
            markdown += "\n"
        
        if dest_info.get('safety_tips'):
            markdown += "**Safety Tips:**\n"
            for tip in dest_info['safety_tips']:
                markdown += f"- {tip}\n"
            markdown += "\n"
        
        if dest_info.get('local_tips'):
            markdown += "**Local Tips:**\n"
            for tip in dest_info['local_tips']:
                markdown += f"- {tip}\n"
            markdown += "\n"
        
        if dest_info.get('emergency_numbers'):
            markdown += f"**Emergency Numbers:** {dest_info['emergency_numbers']}\n\n"
    
    markdown += """
    ---

    ## 🎉 Have a Wonderful Trip!

    *This itinerary was created by your AI Travel Planning Agent*  
    *All prices are estimates and should be verified at time of booking*
    """
    
    state["final_itinerary"] = markdown
    
    # Store in global itinerary content for tools to access
    set_itinerary_content(markdown)
    
    # In conversational mode, go to feedback; otherwise complete
    if state.get("iteration_count", 0) == 0:
        state["next_step"] = "get_feedback"
        print("\n✅ Itinerary created! Getting your feedback...")
    else:
        state["next_step"] = "get_feedback"
        print("\n✅ Itinerary updated based on your feedback!")
    
    return state

