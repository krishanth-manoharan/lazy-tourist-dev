"""
Unified Test Suite for Lazy Tourist Travel Planning Agent

This suite combines all test scenarios:
1. Basic automated conversation
2. Conversational refinement
3. Missing information prompts
"""

from dotenv import load_dotenv
load_dotenv()

from graph import create_travel_agent_graph
from agents.state import TravelState
from unittest.mock import patch
import sys


def create_initial_state(query: str) -> TravelState:
    """Helper to create initial state"""
    return {
        "messages": [],
        "user_query": query,
        "preferences": {},
        "flights": [],
        "return_flights": [],
        "hotels": [],
        "activities": [],
        "destination_info": {},
        "daily_itinerary": [],
        "budget": {},
        "selected_flight": {},
        "selected_return_flight": {},
        "selected_hotel": {},
        "next_step": "",
        "final_itinerary": "",
        "needs_user_input": False,
        "iteration_count": 0,
        "user_satisfied": False,
        "feedback_message": "",
        "conversation_history": []
    }


def run_test(test_name: str, query: str, responses: list, max_steps: int = 30) -> bool:
    """
    Run a test scenario with simulated user inputs
    
    Args:
        test_name: Name of the test
        query: Initial user query
        responses: List of simulated user responses
        max_steps: Maximum steps before timeout
    
    Returns:
        True if test passed, False otherwise
    """
    print("\n" + "="*80)
    print(f"🧪 {test_name}")
    print("="*80)
    print(f"\n📝 Initial Query: {query}\n")
    
    response_iter = iter(responses)
    
    def mock_input(prompt):
        """Mock input function that returns pre-scripted responses"""
        try:
            response = next(response_iter)
            print(f"{prompt}{response}")
            return response
        except StopIteration:
            print(f"{prompt}save")
            return "save"
    
    # Create the agent
    app = create_travel_agent_graph()
    initial_state = create_initial_state(query)
    
    print("🚀 Running agent...\n")
    
    with patch('builtins.input', side_effect=mock_input):
        try:
            step_count = 0
            for step_output in app.stream(initial_state):
                step_count += 1
                
                if isinstance(step_output, dict):
                    if "__end__" in step_output:
                        print(f"\n🏁 Test completed in {step_count} steps")
                        break
                
                if step_count > max_steps:
                    print(f"\n⚠️  Max steps ({max_steps}) reached")
                    break
            
            print("\n" + "="*80)
            print(f"✅ {test_name} - PASSED")
            print("="*80)
            return True
            
        except Exception as e:
            print(f"\n❌ {test_name} - FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_basic_conversation():
    """Test 1: Basic automated conversation"""
    return run_test(
        test_name="BASIC CONVERSATION TEST",
        query="Plan a 3-day trip to Paris for 2 adults, budget $2000, love food",
        responses=["save"]
    )


def test_refinement():
    """Test 2: Conversation with refinement requests"""
    return run_test(
        test_name="REFINEMENT TEST",
        query="4-day Bali trip for 2, budget $2500, love beaches",
        responses=[
            "show me the itinerary",
            "find a cheaper hotel",
            "save"
        ]
    )


def test_missing_info():
    """Test 3: Incomplete query with missing information prompts"""
    return run_test(
        test_name="MISSING INFORMATION TEST",
        query="I want to travel",
        responses=[
            "San Francisco",  # Where from?
            "Tokyo",          # Where to?
            "5",              # How many days?
            "2",              # How many adults?
            "4000",           # Budget?
            "save"            # Save the itinerary
        ]
    )


def test_partial_query():
    """Test 4: Partial query (has destination, missing other info)"""
    return run_test(
        test_name="PARTIAL QUERY TEST",
        query="I want to visit Paris",
        responses=[
            "Boston",   # Where from?
            "3",        # How many days?
            "1",        # How many adults?
            "1500",     # Budget?
            "save"
        ]
    )


def run_all_tests():
    """Run all test scenarios"""
    print("\n" + "🎯"*40)
    print("LAZY TOURIST - UNIFIED TEST SUITE")
    print("🎯"*40)
    
    tests = [
        ("Basic Conversation", test_basic_conversation),
        ("Refinement Flow", test_refinement),
        ("Missing Information", test_missing_info),
        ("Partial Query", test_partial_query)
    ]
    
    results = []
    for test_name, test_func in tests:
        print("\n")
        success = test_func()
        results.append((test_name, success))
        print("\n")
    
    # Print summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = 0
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {name}")
        if success:
            passed += 1
    
    print("\n" + "="*80)
    print(f"Results: {passed}/{len(results)} tests passed")
    print("="*80)
    
    return passed == len(results)


if __name__ == "__main__":
    # Check for specific test argument
    if len(sys.argv) > 1:
        test_arg = sys.argv[1].lower()
        
        if test_arg == "basic":
            success = test_basic_conversation()
        elif test_arg == "refine":
            success = test_refinement()
        elif test_arg == "missing":
            success = test_missing_info()
        elif test_arg == "partial":
            success = test_partial_query()
        else:
            print(f"Unknown test: {test_arg}")
            print("Available tests: basic, refine, missing, partial")
            print("Or run without arguments to run all tests")
            sys.exit(1)
    else:
        # Run all tests
        success = run_all_tests()
    
    sys.exit(0 if success else 1)

