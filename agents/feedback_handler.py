"""User feedback handler for iterative itinerary refinement"""
from agents.state import TravelState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools.itinerary_tools import update_itinerary_content, save_itinerary_to_file
from langgraph.prebuilt import ToolNode
import json

def user_feedback_agent(state: TravelState) -> TravelState:
    """Handle user feedback and determine what to do next using LLM decision"""
    print("\n" + "="*60)
    print("💬 USER FEEDBACK HANDLER")
    print("="*60)
    
    # Check if we already have user feedback from main loop
    user_feedback = state.get("user_feedback_input", "").strip()
    
    # If no feedback yet, signal main.py to collect it
    if not user_feedback:
        # Only show itinerary on the FIRST call (when we're about to ask for input)
        # Don't show it on the second call when we have the input
        show_itinerary = state.get("show_itinerary", True)
        
        # Show itinerary only if flag is True
        if show_itinerary and state.get("final_itinerary"):
            print("\n" + "="*60)
            print("📄 YOUR CURRENT ITINERARY")
            print("="*60)
            print(state.get("final_itinerary", "No itinerary generated yet."))
            print("\n" + "="*60)
        
        state["needs_user_input"] = True
        state["show_itinerary"] = show_itinerary  # Pass flag to main for prompt
        return state
    
    # Clear the feedback input for next iteration
    state["user_feedback_input"] = ""
    state["needs_user_input"] = False
    
    # If empty input, treat as save
    if not user_feedback:
        state["user_satisfied"] = True
        state["next_step"] = "save_and_exit"
        print("\n✅ Great! Saving your itinerary...")
        return state
    
    # Store in conversation history
    conversation_history = state.get("conversation_history", [])
    conversation_history.append(f"User: {user_feedback}")
    
    # Use LLM to analyze feedback and decide action
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    system_prompt = """You are a travel planning assistant analyzing user feedback.

Your job is to determine the user's intent and decide what action to take:

1. **CLARIFY**: If the user is asking a basic clarification question that doesn't require itinerary changes
   - Questions about the trip, destination, weather, culture, etc.
   - General information requests
   - Simple "what" or "how" questions that can be answered directly

2. **REFINE**: If the user wants to modify or change the itinerary
   - Requests to add/remove activities
   - Changes to hotels, flights, budget
   - Modifications to dates, duration, or preferences
   - Any request that requires updating the itinerary

3. **SAVE**: If the user is satisfied and wants to save/finish
   - Expressions of satisfaction ("looks good", "perfect", "save", etc.)
   - Confirmation they're happy with the itinerary
   - Requests to finish or exit

Return a JSON object with:
{
    "action": "clarify" | "refine" | "save",
    "reasoning": "Brief explanation of why this action was chosen",
    "response": "If action is 'clarify', provide a helpful response to the user's question. If action is 'refine', provide a brief acknowledgment. If action is 'save', provide a confirmation message."
}
"""
    
    current_itinerary = state.get("final_itinerary", "")
    prefs = state.get("preferences", {})
    
    # Build conversation context (use history BEFORE current message for prompt)
    conversation_context = ""
    if conversation_history:
        # Use all but the last message (which is the current user feedback)
        history_for_prompt = conversation_history[:-1] if len(conversation_history) > 0 else []
        if history_for_prompt:
            conversation_context = "\n\nPrevious conversation:\n" + "\n".join(history_for_prompt[-6:])  # Last 3 exchanges (6 messages)
    
    user_message = f"""
Current itinerary context:
- Destination: {prefs.get('destination', 'N/A')}
- Duration: {prefs.get('duration_days', 'N/A')} days
- Budget: ${prefs.get('budget', 'N/A')}
{conversation_context}

Current user feedback: "{user_feedback}"

What action should be taken? Analyze if this is a clarification question, a refinement request, or a save request.
"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    try:
        response = model.invoke(messages)
        decision = json.loads(response.content)
        
        action = decision.get("action", "refine").lower()
        reasoning = decision.get("reasoning", "")
        response_text = decision.get("response", "")
        
        print(f"\n🤔 Analysis: {reasoning}")
        
        if action == "save":
            state["user_satisfied"] = True
            state["next_step"] = "save_and_exit"
            state["show_itinerary"] = True  # Reset for next time
            state["assistant_response"] = ""  # Clear response
            if response_text:
                print(f"\n✅ {response_text}")
            else:
                print("\n✅ Great! Saving your itinerary...")
            return state
        
        elif action == "clarify":
            # Store assistant response and loop back to get_feedback
            assistant_msg = response_text if response_text else "I'm here to help! What would you like to know?"
            state["assistant_response"] = assistant_msg
            state["show_itinerary"] = False  # Don't show itinerary on next loop
            state["next_step"] = "get_feedback"  # Loop back to same node
            conversation_history.append(f"Assistant: {assistant_msg}")
            state["conversation_history"] = conversation_history
            
            # Print the clarification response
            print(f"\n💭 {assistant_msg}")
            print("\n" + "="*60)
            
            return state
        
        else:  # refine
            state["user_satisfied"] = False
            state["feedback_message"] = user_feedback
            state["next_step"] = "refine_itinerary"
            state["show_itinerary"] = True  # Reset for next time after refinement
            state["assistant_response"] = ""  # Clear response
            conversation_history.append(f"Assistant: {response_text if response_text else 'Working on your changes...'}")
            state["conversation_history"] = conversation_history
            
            if response_text:
                print(f"\n🔄 {response_text}")
            else:
                print(f"\n🔄 I'll work on: {user_feedback}")
            
            return state
    
    except (json.JSONDecodeError, Exception) as e:
        print(f"\n⚠️  Error analyzing feedback: {e}")
        print("⚠️  Defaulting to refinement...")
        # Fallback to refinement
        state["user_satisfied"] = False
        state["feedback_message"] = user_feedback
        state["next_step"] = "refine_itinerary"
        state["show_itinerary"] = True
        state["assistant_response"] = ""
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

    IMPORTANT: Set "requires_new_search" to TRUE if ANY of these change:
    - Duration/number of days (affects hotel nights and return flight dates)
    - Budget (need to find flights/hotels in new price range)
    - Number of travelers (affects flight/hotel pricing and availability)
    - Dates (departure or return dates change)
    - Hotel star rating preference (need to search different tier)
    
    Set "requires_new_search" to FALSE only if:
    - Only activities/interests are changing
    - Minor adjustments to existing itinerary
    - Just want to see different activity options

    Return a JSON object with:
    {
        "changes_needed": ["list of specific changes to make"],
        "requires_new_search": false,  // true if need to search flights/hotels again (see rules above)
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
    
    try:
        response = model.invoke(messages)
    except Exception as e:
        print(f"\n❌ Error during refinement: {e}")
        print("⚠️  Exiting...")
        state["next_step"] = "end"
        return state
    
    try:
        refinement = json.loads(response.content)
        
        if refinement.get("clarifying_question"):
            print(f"\n❓ {refinement['clarifying_question']}")
            print("\n⚠️  Feedback unclear. Saving itinerary as-is...")
            state["next_step"] = "save_and_exit"
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
        
        # Force re-search if critical preferences changed (override LLM decision for safety)
        critical_changes = ["duration_days", "budget", "num_adults", "num_children", "min_hotel_stars"]
        force_research = any(key in updated_prefs and updated_prefs[key] is not None for key in critical_changes)
        
        # If requires new search, go back to searching
        if refinement.get("requires_new_search") or force_research:
            if force_research and not refinement.get("requires_new_search"):
                print("\n⚠️  Critical preference changed - forcing new search for accurate results...")
            state["next_step"] = "search_flights"
            print("\n🔍 Will perform new searches based on your requirements...")
        else:
            # Otherwise, just recompile itinerary with modifications
            state["next_step"] = "compile_itinerary"
            print("\n📋 Updating your itinerary...")
        
    except json.JSONDecodeError:
        # Fallback: try to proceed with refinement anyway
        print(f"\n⚠️  Could not parse refinement response, proceeding with basic updates...")
        print(f"💭 I understand you want: {feedback}")
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

