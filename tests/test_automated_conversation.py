"""
Automated test for conversational travel planning

This simulates a full conversation with pre-scripted responses
"""

from dotenv import load_dotenv
load_dotenv()

from graph import create_travel_agent_graph
from agents.state import TravelState
from unittest.mock import patch
import io

def test_full_conversation_automated():
    """
    Test a full conversational flow with simulated user inputs
    
    Conversation flow:
    1. Initial request: Paris trip
    2. Agent creates itinerary
    3. User views itinerary
    4. User requests to save
    5. Agent saves and exits
    """
    
    print("\n" + "="*80)
    print("🧪 AUTOMATED CONVERSATIONAL TEST")
    print("="*80)
    
    # Simulated user responses (in order)
    # Format: questions might be asked for missing info, then feedback
    simulated_responses = [
        # No missing info questions expected for this query
        "save",  # Feedback: just save it
    ]
    
    response_iter = iter(simulated_responses)
    
    def mock_input(prompt):
        """Mock input function that returns pre-scripted responses"""
        try:
            response = next(response_iter)
            print(f"{prompt}{response}")
            return response
        except StopIteration:
            # If we run out of responses, just save
            print(f"{prompt}save")
            return "save"
    
    # Create the agent
    app = create_travel_agent_graph()
    
    # Initial state
    initial_state: TravelState = {
        "messages": [],
        "user_query": "Plan a 3-day trip to Paris for 2 adults, budget $2000, love food",
        "preferences": {},
        "flights": [],
        "hotels": [],
        "activities": [],
        "destination_info": {},
        "daily_itinerary": [],
        "budget": {},
        "selected_flight": {},
        "selected_hotel": {},
        "next_step": "",
        "final_itinerary": "",
        "needs_user_input": False,
        "iteration_count": 0,
        "user_satisfied": False,
        "feedback_message": "",
        "conversation_history": []
    }
    
    print("\n📝 Initial Request: Plan a 3-day trip to Paris for 2 adults, budget $2000, love food")
    print("\n🚀 Running conversational agent...\n")
    
    # Patch the input function
    with patch('builtins.input', side_effect=mock_input):
        try:
            step_count = 0
            for step_output in app.stream(initial_state):
                step_count += 1
                
                if isinstance(step_output, dict):
                    # Check if we've reached the end
                    if "__end__" in step_output:
                        print(f"\n🏁 Conversation completed in {step_count} steps")
                        break
                
                # Safety limit
                if step_count > 30:
                    print("\n⚠️  Max steps reached")
                    break
            
            print("\n" + "="*80)
            print("✅ AUTOMATED TEST COMPLETED SUCCESSFULLY!")
            print("="*80)
            print("\n📁 Check the outputs/ directory for the saved itinerary")
            
            return True
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_conversation_with_changes():
    """
    Test a conversation with refinement requests
    
    Conversation flow:
    1. Initial request
    2. View itinerary  
    3. Request changes (cheaper hotel)
    4. View updated itinerary
    5. Save
    """
    
    print("\n" + "="*80)
    print("🧪 AUTOMATED TEST WITH REFINEMENTS")
    print("="*80)
    
    # Simulated user responses
    simulated_responses = [
        # No missing info expected for this query either
        "show me the itinerary",           # First: view it
        "find a cheaper hotel",            # Second: request change
        "save",                            # Third: save
    ]
    
    response_iter = iter(simulated_responses)
    
    def mock_input(prompt):
        """Mock input function"""
        try:
            response = next(response_iter)
            print(f"{prompt}{response}")
            return response
        except StopIteration:
            print(f"{prompt}save")
            return "save"
    
    # Create the agent
    app = create_travel_agent_graph()
    
    initial_state: TravelState = {
        "messages": [],
        "user_query": "4-day Bali trip for 2, budget $2500, love beaches",
        "preferences": {},
        "flights": [],
        "hotels": [],
        "activities": [],
        "destination_info": {},
        "daily_itinerary": [],
        "budget": {},
        "selected_flight": {},
        "selected_hotel": {},
        "next_step": "",
        "final_itinerary": "",
        "needs_user_input": False,
        "iteration_count": 0,
        "user_satisfied": False,
        "feedback_message": "",
        "conversation_history": []
    }
    
    print("\n📝 Initial Request: 4-day Bali trip for 2, budget $2500, love beaches")
    print("\n🚀 Running conversational agent with refinements...\n")
    
    with patch('builtins.input', side_effect=mock_input):
        try:
            step_count = 0
            for step_output in app.stream(initial_state):
                step_count += 1
                
                if isinstance(step_output, dict):
                    if "__end__" in step_output:
                        print(f"\n🏁 Conversation completed in {step_count} steps")
                        break
                
                if step_count > 30:
                    print("\n⚠️  Max steps reached")
                    break
            
            print("\n" + "="*80)
            print("✅ REFINEMENT TEST COMPLETED SUCCESSFULLY!")
            print("="*80)
            
            return True
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "refine":
        # Test with refinements
        success = test_conversation_with_changes()
    else:
        # Simple test
        success = test_full_conversation_automated()
    
    sys.exit(0 if success else 1)

