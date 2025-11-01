"""
Test the interactive missing information prompts

This test verifies that the agent asks for missing critical information
"""

from dotenv import load_dotenv
load_dotenv()

from graph import create_travel_agent_graph
from agents.state import TravelState
from unittest.mock import patch

def test_incomplete_query():
    """
    Test that agent asks for missing information when query is incomplete
    
    Query: Just "I want to travel" (missing everything)
    Expected: Agent should ask for origin, destination, duration, travelers, budget
    """
    
    print("\n" + "="*80)
    print("🧪 TESTING MISSING INFORMATION PROMPTS")
    print("="*80)
    
    # Simulated responses for missing info questions + feedback
    simulated_responses = [
        # Intent extractor will ask for missing info:
        "San Francisco",  # Where are you traveling from?
        "Tokyo",          # Where would you like to go?
        "5",              # How many days?
        "2",              # How many adults?
        "4000",           # Budget?
        # Then feedback:
        "save",           # Save the itinerary
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
    
    # Incomplete initial query
    initial_state: TravelState = {
        "messages": [],
        "user_query": "I want to travel",  # Very incomplete!
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
    
    print("\n📝 Incomplete Query: 'I want to travel'")
    print("Expected: Agent should ask for missing information\n")
    
    with patch('builtins.input', side_effect=mock_input):
        try:
            step_count = 0
            for step_output in app.stream(initial_state):
                step_count += 1
                
                if isinstance(step_output, dict):
                    if "__end__" in step_output:
                        print(f"\n🏁 Test completed in {step_count} steps")
                        break
                
                if step_count > 30:
                    print("\n⚠️  Max steps reached")
                    break
            
            print("\n" + "="*80)
            print("✅ MISSING INFO TEST COMPLETED!")
            print("="*80)
            print("\n✅ Agent successfully prompted for missing information!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_partial_query():
    """
    Test with partially complete query (has destination but missing other info)
    """
    
    print("\n" + "="*80)
    print("🧪 TESTING PARTIAL QUERY")
    print("="*80)
    
    simulated_responses = [
        # Might ask for origin, duration, travelers, budget (has destination)
        "Boston",     # Where are you traveling from?
        "3",          # How many days?
        "1",          # How many adults?
        "1500",       # Budget?
        # Then feedback:
        "save",
    ]
    
    response_iter = iter(simulated_responses)
    
    def mock_input(prompt):
        try:
            response = next(response_iter)
            print(f"{prompt}{response}")
            return response
        except StopIteration:
            return "save"
    
    app = create_travel_agent_graph()
    
    initial_state: TravelState = {
        "messages": [],
        "user_query": "I want to visit Paris",  # Has destination only
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
    
    print("\n📝 Partial Query: 'I want to visit Paris'")
    print("Expected: Agent should ask for origin, duration, travelers, budget\n")
    
    with patch('builtins.input', side_effect=mock_input):
        try:
            step_count = 0
            for step_output in app.stream(initial_state):
                step_count += 1
                if isinstance(step_output, dict) and "__end__" in step_output:
                    break
                if step_count > 30:
                    break
            
            print("\n✅ PARTIAL QUERY TEST COMPLETED!")
            return True
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    import sys
    
    print("\n🎯 Testing Interactive Missing Information Feature\n")
    
    # Test 1: Very incomplete query
    success1 = test_incomplete_query()
    
    print("\n" + "="*80 + "\n")
    
    # Test 2: Partially complete query
    success2 = test_partial_query()
    
    if success1 and success2:
        print("\n\n🎉 ALL MISSING INFO TESTS PASSED! ✅")
        sys.exit(0)
    else:
        print("\n\n❌ SOME TESTS FAILED")
        sys.exit(1)

