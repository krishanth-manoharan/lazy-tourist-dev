"""User feedback handler for iterative itinerary refinement"""
from agents.state import TravelState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools.itinerary_tools import update_itinerary_content, save_itinerary_to_file
from langgraph.prebuilt import ToolNode
import json

def user_feedback_agent(state: TravelState) -> TravelState:
    """Handle user feedback and determine what to do next"""
    print("\n" + "="*60)
    print("💬 USER FEEDBACK HANDLER - Waiting for your input...")
    print("="*60)
    
    # Show current itinerary summary
    if state.get("final_itinerary"):
        print("\n📋 Current itinerary is ready for your review!")
        print("\nYou can:")
        print("  • Ask to see the full itinerary")
        print("  • Request changes (e.g., 'add more food activities', 'find cheaper hotels')")
        print("  • Say 'save' or 'looks good' to save and finish")
        print("  • Ask questions about the trip")
    
    # Get user input
    user_feedback = input("\n💬 Your feedback (or 'save' to finish): ").strip()
    
    if not user_feedback:
        user_feedback = "show me the itinerary"
    
    # Store in conversation history
    conversation_history = state.get("conversation_history", [])
    conversation_history.append(f"User: {user_feedback}")
    state["conversation_history"] = conversation_history
    
    # Check if user wants to save
    save_keywords = ['save', 'looks good', 'perfect', 'done', 'finish', 'exit', 'great', "i'm happy", "im happy"]
    if any(keyword in user_feedback.lower() for keyword in save_keywords):
        state["user_satisfied"] = True
        state["next_step"] = "save_and_exit"
        print("\n✅ Great! Saving your itinerary...")
        return state
    
    # Check if user wants to see the itinerary
    show_keywords = ['show', 'display', 'see', 'view', 'itinerary', 'what do you have']
    if any(keyword in user_feedback.lower() for keyword in show_keywords):
        print("\n" + "="*60)
        print("📄 YOUR CURRENT ITINERARY")
        print("="*60)
        print(state.get("final_itinerary", "No itinerary generated yet."))
        print("\n" + "="*60)
        state["next_step"] = "get_feedback"
        state["feedback_message"] = "Itinerary displayed. What would you like to change?"
        return state
    
    # User wants modifications
    state["user_satisfied"] = False
    state["feedback_message"] = user_feedback
    state["next_step"] = "refine_itinerary"
    
    print(f"\n🔄 I'll work on: {user_feedback}")
    
    return state

def refine_itinerary_agent(state: TravelState) -> TravelState:
    """Refine the itinerary based on user feedback"""
    print("\n" + "="*60)
    print("🔧 REFINING ITINERARY - Based on your feedback...")
    print("="*60)
    
    feedback = state.get("feedback_message", "")
    current_itinerary = state.get("final_itinerary", "")
    prefs = state.get("preferences", {})
    
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    system_prompt = """You are a travel planning assistant helping to refine an itinerary based on user feedback.

The user has provided feedback about their current itinerary. Your job is to:
1. Understand what they want to change
2. Extract any updated preferences (budget, duration, interests, etc.)
3. Suggest specific modifications
4. Update the relevant parts of the itinerary

Be helpful and conversational. If the request is:
- About budget: Extract the new budget amount and suggest cheaper/more expensive alternatives
- About duration: Extract the new duration and adjust the itinerary
- About activities: Add more of the requested type or change existing ones
- About hotels: Suggest different accommodations
- About flights: Mention alternative options
- Unclear: Ask clarifying questions

Return a JSON object with:
{
    "changes_needed": ["list of specific changes to make"],
    "requires_new_search": false,  // true if need to search flights/hotels again
    "clarifying_question": null,  // or a question if feedback is unclear
    "updated_summary": "Brief summary of what will change",
    "updated_preferences": {  // any preference changes extracted from feedback
        "budget": null,  // new budget if mentioned
        "duration_days": null,  // new duration if mentioned
        "interests": null,  // updated interests if mentioned (full list)
        "min_hotel_stars": null,  // updated hotel preference
        "num_adults": null,  // updated number of adults
        "num_children": null  // updated number of children
    }
}

Only include fields in updated_preferences that the user actually wants to change.
"""
    
    user_message = f"""
Current itinerary summary:
- Destination: {prefs.get('destination', 'N/A')}
- Budget: ${prefs.get('budget', 0)}
- Duration: {prefs.get('duration_days', 0)} days
- Travelers: {prefs.get('num_adults', 2)} adults, {prefs.get('num_children', 0)} children
- Interests: {', '.join(prefs.get('interests', []))}
- Hotel preference: {prefs.get('min_hotel_stars', 3)}+ stars

User feedback: "{feedback}"

What changes should be made to address this feedback? Extract any updated preference values.
"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    response = model.invoke(messages)
    
    try:
        refinement = json.loads(response.content)
        
        if refinement.get("clarifying_question"):
            print(f"\n❓ {refinement['clarifying_question']}")
            state["next_step"] = "get_feedback"
            return state
        
        # Update preferences based on feedback
        updated_prefs = refinement.get("updated_preferences", {})
        preferences = state.get("preferences", {})
        
        preference_changes = []
        for key, value in updated_prefs.items():
            if value is not None and key in preferences:
                old_value = preferences.get(key)
                preferences[key] = value
                preference_changes.append(f"{key}: {old_value} → {value}")
                
                # If duration changed, update dates
                if key == "duration_days":
                    from datetime import datetime, timedelta
                    dep_date = datetime.strptime(preferences["departure_date"], "%Y-%m-%d")
                    ret_date = dep_date + timedelta(days=value)
                    preferences["return_date"] = ret_date.strftime("%Y-%m-%d")
                    preference_changes.append(f"return_date updated to {preferences['return_date']}")
                
                # If travelers changed, update total
                if key in ["num_adults", "num_children"]:
                    preferences["total_passengers"] = preferences.get("num_adults", 2) + preferences.get("num_children", 0)
                    preference_changes.append(f"total_passengers: {preferences['total_passengers']}")
        
        state["preferences"] = preferences
        
        if preference_changes:
            print(f"\n🔄 Updated preferences:")
            for change in preference_changes:
                print(f"   • {change}")
        
        print(f"\n📝 Changes to make:")
        for i, change in enumerate(refinement.get("changes_needed", []), 1):
            print(f"   {i}. {change}")
        
        print(f"\n💡 {refinement.get('updated_summary', '')}")
        
        # If requires new search, go back to searching
        if refinement.get("requires_new_search"):
            state["next_step"] = "search_flights"
            print("\n🔍 Will perform new searches based on your requirements...")
        else:
            # Otherwise, just recompile itinerary with modifications
            state["next_step"] = "compile_itinerary"
            print("\n📋 Updating your itinerary...")
        
    except json.JSONDecodeError:
        # Fallback: just show what we understood
        print(f"\n💭 I understand you want: {feedback}")
        print("Let me regenerate the itinerary with your preferences in mind...")
        state["next_step"] = "compile_itinerary"
    
    return state

def save_itinerary_agent(state: TravelState) -> TravelState:
    """Save the final itinerary and prepare to exit"""
    print("\n" + "="*60)
    print("💾 SAVING YOUR ITINERARY...")
    print("="*60)
    
    destination = state.get("preferences", {}).get("destination", "trip")
    final_itinerary = state.get("final_itinerary", "")
    
    # Use the tool to save
    from tools.itinerary_tools import set_itinerary_content
    set_itinerary_content(final_itinerary)
    
    result = save_itinerary_to_file.invoke({
        "filename": "",
        "destination": destination
    })
    
    print(f"\n{result}")
    
    # Show final message
    print("\n" + "="*60)
    print("🎉 YOUR TRIP IS ALL SET!")
    print("="*60)
    print(f"\n📍 Destination: {destination}")
    print(f"📅 Duration: {state.get('preferences', {}).get('duration_days', 'N/A')} days")
    print(f"💰 Budget: ${state.get('preferences', {}).get('budget', 'N/A')}")
    print(f"\n✈️ Have an amazing trip! Safe travels! 🌍")
    
    state["next_step"] = "end"
    
    return state

