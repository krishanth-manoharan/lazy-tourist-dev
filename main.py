"""Main application for the Travel Planning Agent"""
from dotenv import load_dotenv
from graph import create_travel_agent_graph, visualize_graph
from agents.state import TravelState

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

def run_travel_agent(show_graph: bool = False, dark_graph: bool = False):
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
        visualize_graph(app, dark_mode=dark_graph)
    
    # Initialize state
    initial_state: TravelState = {
        "messages": [],
        "user_query": user_query,
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
        "conversation_history": [f"User: {user_query}"],  # Include initial query in history
        "show_itinerary": True,
        "assistant_response": "",
        "user_feedback_input": ""
    }
    
    # Run the agent
    try:
        print("\n" + "="*60)
        print("🎬 STARTING TRAVEL PLANNING...")
        print("="*60)
        
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        is_first_run = True
        pending_state_update = None  # Track state updates from previous iteration
        
        # Use a thread ID for checkpointing - allows resuming from where we left off
        thread_config = {"configurable": {"thread_id": "travel_planning_session"}}
        
        # Loop until we reach the end or max iterations
        while iteration < max_iterations:
            iteration += 1
            needs_input = False
            last_node = None  # Track which node we're at
            state_update = None  # Track state updates for current iteration
            
            # Stream the graph execution with checkpointing
            # First iteration: pass full initial state (starts from START)
            # Subsequent iterations: update checkpoint and pass None to resume
            if is_first_run:
                stream_input = initial_state
                is_first_run = False
            else:
                # Update the checkpoint with state data from last iteration, then resume
                if pending_state_update:
                    app.update_state(thread_config, pending_state_update, as_node="get_feedback" if "user_feedback_input" in pending_state_update else "extract_intent")
                stream_input = None  # Resume from checkpoint
            
            for step_output in app.stream(stream_input, thread_config, stream_mode="updates"):
                # The stream yields state updates per node
                if isinstance(step_output, dict):
                    # Check if any step needs user input
                    for node_name, node_state in step_output.items():
                        last_node = node_name
                        
                        if node_name == "extract_intent":
                            if node_state.get("needs_user_input"):
                                # Display the LLM's question
                                feedback_msg = node_state.get("feedback_message", "")
                                if feedback_msg:
                                    print(f"\n{feedback_msg}")
                                
                                # Get user's response
                                user_response = input("\n💬 Your response: ").strip()
                                
                                # Update conversation history with the exchange
                                conversation_history = node_state.get("conversation_history", [])
                                conversation_history.append(f"Assistant: {feedback_msg}")
                                conversation_history.append(f"User: {user_response}")
                                
                                # Prepare state update for next iteration (only the changes)
                                state_update = {
                                    "conversation_history": conversation_history,
                                    "needs_user_input": False
                                }
                                
                                needs_input = True
                                break
                        
                        elif node_name == "get_feedback":
                            if node_state.get("needs_user_input"):
                                # Check if we should show itinerary or just get response
                                show_itinerary = node_state.get("show_itinerary", True)
                                
                                # Display assistant response if it exists (for clarification)
                                assistant_response = node_state.get("assistant_response", "")
                                if assistant_response and not show_itinerary:
                                    # Already printed by the agent, just get input
                                    pass
                                
                                # Get user feedback with appropriate prompt
                                try:
                                    if show_itinerary:
                                        user_feedback = input("\n💬 Your feedback: ").strip()
                                    else:
                                        user_feedback = input("\n💬 Your response: ").strip()
                                except (EOFError, KeyboardInterrupt):
                                    print("\n⚠️  Input error. Exiting...")
                                    state_update = {
                                        "next_step": "end",
                                        "needs_user_input": False
                                    }
                                    needs_input = True
                                    break
                                
                                # Prepare state update with user feedback
                                state_update = {
                                    "user_feedback_input": user_feedback,
                                    "needs_user_input": False
                                }
                                
                                needs_input = True
                                break
                
                if needs_input:
                    break
            
            # Save state update for next iteration
            if state_update:
                pending_state_update = state_update
            
            # If we didn't need input, we're done
            if not needs_input:
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
        "--dark-graph",
        action="store_true",
        help="Use dark mode for graph visualization (requires Pillow)"
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
    run_travel_agent(show_graph=args.show_graph, dark_graph=args.dark_graph)

if __name__ == "__main__":
    main()

