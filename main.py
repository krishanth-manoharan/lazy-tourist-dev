"""Main application for the Travel Planning Agent"""
from dotenv import load_dotenv
from graph import create_travel_agent_graph, visualize_graph
from agents.state import TravelState
import sys
import os

# Load environment variables
load_dotenv()

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🌍 LAZY TOURIST - AI Travel Planner 🌍              ║
║                                                              ║
║         Your Personal AI Travel Planning Assistant           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """Print help information"""
    help_text = """
📖 HOW TO USE:

This is an INTERACTIVE travel planning experience!

1️⃣  Start by describing your dream trip
2️⃣  Review the generated itinerary
3️⃣  Request changes and refinements
4️⃣  When you're happy, say "save" to finalize

EXAMPLE CONVERSATION:

  You: "Plan a 5-day trip to Paris for 2, budget $3000, love food"
  
  🤖 Agent: [Creates initial itinerary]
  
  You: "Show me the itinerary"
  
  🤖 Agent: [Displays full itinerary]
  
  You: "Add more food activities and find a cheaper hotel"
  
  🤖 Agent: [Updates itinerary]
  
  You: "Perfect! Save it"
  
  🤖 Agent: [Saves to outputs/ directory] ✅

TIPS:
  • Be specific about what you want to change
  • You can ask questions about the trip
  • Say "save", "looks good", or "perfect" when satisfied
  • Type "exit" to quit without saving

Ready to plan your next adventure? 🎒
    """
    print(help_text)

def run_travel_agent(show_graph: bool = False):
    """Run the travel agent in interactive mode"""
    
    print_banner()
    print("\n" + "="*60)
    print("🚀 INTERACTIVE TRAVEL PLANNING")
    print("="*60)
    
    # Get initial travel request
    print("\n💬 Let's plan your perfect trip!")
    user_query = input("\n✈️  Describe your dream trip: ").strip()
    
    if not user_query:
        user_query = "Plan a 5-day trip to Paris for 2 adults, budget $3000, love food and history"
        print(f"Using example: {user_query}")
    
    # Check for exit
    if user_query.lower() in ['exit', 'quit', 'q']:
        print("\n👋 Maybe next time! Safe travels! 🌍")
        return
    
    # Create the agent graph
    print("\n🔧 Initializing travel planning system...")
    app = create_travel_agent_graph()
    
    # Optionally visualize the graph
    if show_graph:
        visualize_graph(app)
    
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
    
    # Run the agent
    try:
        print("\n" + "="*60)
        print("🎬 STARTING TRAVEL PLANNING...")
        print("="*60)
        
        # Stream the graph execution
        for step_output in app.stream(initial_state):
            # The stream yields state updates
            if isinstance(step_output, dict):
                # Check if we've reached the end
                if "__end__" in step_output:
                    break
        
        print("\n" + "="*60)
        print("✅ TRAVEL PLANNING COMPLETE!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Planning interrupted. Your progress has not been saved.")
        print("👋 Thanks for using Lazy Tourist!")
    except Exception as e:
        print(f"\n❌ Error running travel agent: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Lazy Tourist - Interactive AI Travel Planning Agent"
    )
    parser.add_argument(
        "--show-graph", 
        "-g", 
        action="store_true", 
        help="Show the agent graph visualization"
    )
    parser.add_argument(
        "--help-guide",
        action="store_true",
        help="Show detailed usage guide"
    )
    
    args = parser.parse_args()
    
    if args.help_guide:
        print_banner()
        print_help()
        return
    
    # Run interactive mode
    run_travel_agent(show_graph=args.show_graph)

if __name__ == "__main__":
    main()

