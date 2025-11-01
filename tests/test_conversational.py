"""
Test the conversational travel planning agent

This test simulates a conversational interaction with the agent
"""

from dotenv import load_dotenv
load_dotenv()

from graph import create_travel_agent_graph
from agents.state import TravelState

def simulate_conversation():
    """Simulate a conversational travel planning session"""
    
    print("\n" + "="*80)
    print("🧪 TESTING CONVERSATIONAL TRAVEL AGENT")
    print("="*80)
    
    # Create the agent
    app = create_travel_agent_graph()
    
    # Initial request
    user_query = "Plan a 5-day trip to Paris for 2 adults, budget $3000, love food and history"
    
    print(f"\n📝 Initial Request: {user_query}")
    
    # Initialize state
    initial_state: TravelState = {
        "messages": [],
        "user_query": user_query,
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
    
    print("\n🚀 Running agent graph...")
    print("="*80)
    
    try:
        # Run the graph
        step_count = 0
        for step_output in app.stream(initial_state):
            step_count += 1
            print(f"\n--- Step {step_count} ---")
            
            if isinstance(step_output, dict):
                # Show which node executed
                for node_name, node_state in step_output.items():
                    if node_name != "__end__":
                        print(f"✓ Executed: {node_name}")
                        if "next_step" in node_state:
                            print(f"  Next: {node_state['next_step']}")
                
                # Check if we've reached the end
                if "__end__" in step_output:
                    print("\n🏁 Reached end of graph")
                    break
            
            # Limit iterations for testing
            if step_count > 20:
                print("\n⚠️  Max iterations reached (safety limit)")
                break
        
        print("\n" + "="*80)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_basic_flow():
    """Test the basic flow without interaction"""
    print("\n🧪 Testing basic agent flow (automated)...\n")
    
    from agents.intent_extractor import extract_intent
    from agents.search_agents import destination_research_agent, flight_search_agent
    from agents.itinerary_compiler import compile_itinerary, format_final_itinerary
    
    # Create minimal state
    state: TravelState = {
        "messages": [],
        "user_query": "3-day Paris trip for 2, budget $2000",
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
    
    # Test intent extraction
    print("1. Testing intent extraction...")
    state = extract_intent(state)
    assert "preferences" in state
    assert state["preferences"].get("destination")
    print(f"   ✓ Extracted destination: {state['preferences']['destination']}")
    
    # Test destination research
    print("\n2. Testing destination research...")
    state = destination_research_agent(state)
    assert "destination_info" in state
    print(f"   ✓ Got destination info")
    
    # Test flight search
    print("\n3. Testing flight search...")
    state = flight_search_agent(state)
    assert "flights" in state
    print(f"   ✓ Found {len(state.get('flights', []))} flights")
    
    print("\n✅ All basic tests passed!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "basic":
        # Run basic tests
        test_basic_flow()
    else:
        # Run full simulation
        # Note: This will require manual input at the feedback stage
        print("\n⚠️  NOTE: This test will pause for user input at the feedback stage.")
        print("    You can type 'save' to complete the test, or provide feedback.\n")
        
        input("Press Enter to continue...")
        simulate_conversation()

