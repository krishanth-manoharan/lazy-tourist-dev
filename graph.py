"""LangGraph orchestration for Travel Planning Agent"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agents.state import TravelState
from agents.intent_extractor import extract_intent
from agents.search_agents import (
    destination_research_agent,
    flight_search_agent,
    hotel_search_agent,
    activity_research_agent
)
from agents.itinerary_compiler import compile_itinerary, format_final_itinerary
from agents.feedback_handler import (
    user_feedback_agent,
    refine_itinerary_agent,
    save_itinerary_agent
)

def create_travel_agent_graph():
    """Create the travel planning agent graph with conversational feedback loop"""
    
    graph = StateGraph(TravelState)
    
    # Add all agent nodes
    graph.add_node("extract_intent", extract_intent)
    graph.add_node("research_destination", destination_research_agent)
    graph.add_node("search_flights", flight_search_agent)
    graph.add_node("search_hotels", hotel_search_agent)
    graph.add_node("search_activities", activity_research_agent)
    graph.add_node("compile_itinerary", compile_itinerary)
    graph.add_node("format_output", format_final_itinerary)
    graph.add_node("get_feedback", user_feedback_agent)
    graph.add_node("refine_itinerary", refine_itinerary_agent)
    graph.add_node("save_and_exit", save_itinerary_agent)
    
    # Define routing functions
    def route_after_intent(state: TravelState) -> str:
        """Route after intent extraction - check if we need more info"""
        next_step = state.get("next_step", "research_destination")
        
        if next_step == "collect_more_info":
            return "extract_intent"  # Loop back to collect more info
        else:
            return "research_destination"
    
    def route_after_feedback(state: TravelState) -> str:
        """Route based on user feedback
        
        The feedback handler uses LLM to decide action:
        - get_feedback: Clarification question - loop back to show assistant response
        - save_and_exit: User wants to save and finish
        - refine_itinerary: User wants modifications (will return to feedback after refinement)
        - end: Error occurred, exit
        """
        next_step = state.get("next_step", "save_and_exit")
        
        if next_step == "get_feedback":
            return "get_feedback"  # Loop back for clarification
        elif next_step == "save_and_exit":
            return "save_and_exit"
        elif next_step == "refine_itinerary":
            return "refine_itinerary"
        elif next_step == "end":
            return "end"
        else:
            # Default to save if unclear
            return "save_and_exit"
    
    def route_after_refinement(state: TravelState) -> str:
        """Route after refinement decision"""
        next_step = state.get("next_step", "format_output")
        
        if next_step == "search_flights":
            return "search_flights"
        elif next_step == "format_output":
            return "format_output"
        else:
            # Fallback to compile_itinerary for backward compatibility
            return "compile_itinerary"
    
    # Build the graph
    # Initial flow: intent -> (loop back to itself or proceed to research_destination)
    graph.add_edge(START, "extract_intent")
    
    # Conditional routing after intent extraction
    graph.add_conditional_edges(
        "extract_intent",
        route_after_intent,
        {
            "extract_intent": "extract_intent",       # Loop back to collect more info
            "research_destination": "research_destination"  # All info present
        }
    )
    
    # Continue with normal flow
    graph.add_edge("research_destination", "search_flights")
    graph.add_edge("search_flights", "search_hotels")
    graph.add_edge("search_hotels", "search_activities")
    graph.add_edge("search_activities", "compile_itinerary")
    graph.add_edge("compile_itinerary", "format_output")
    
    # After formatting, always go to feedback (itinerary is shown by default)
    graph.add_edge("format_output", "get_feedback")
    
    # Feedback handler: uses LLM to decide action
    # Can loop back to itself for clarification, or proceed to refine/save
    graph.add_conditional_edges(
        "get_feedback",
        route_after_feedback,
        {
            "get_feedback": "get_feedback",       # Loop back for clarification (shows assistant response only)
            "refine_itinerary": "refine_itinerary",  # Go to refinement (will return to feedback after)
            "save_and_exit": "save_and_exit",    # Save and exit
            "end": END                            # End on error
        }
    )
    
    # After refinement, decide whether to re-search, recompile, or just reformat
    # All paths eventually return to get_feedback (which shows updated itinerary by default)
    graph.add_conditional_edges(
        "refine_itinerary",
        route_after_refinement,
        {
            "search_flights": "search_flights",      # Re-do searches (flows: flights->hotels->activities->compile->format->feedback)
            "compile_itinerary": "compile_itinerary",  # Recompile (flows: compile->format->feedback)
            "format_output": "format_output"          # Just reformat with user feedback (flows: format->feedback)
        }
    )
    
    # After saving, end
    graph.add_edge("save_and_exit", END)
    
    # Compile with checkpointing to enable resuming from where we left off
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)

def visualize_graph(app, output_file="travel_agent_graph.png"):
    """Generate and save the graph visualization"""
    import subprocess
    
    try:
        # Get the graph image
        image_data = app.get_graph().draw_mermaid_png()
        
        # Save to file
        with open(output_file, 'wb') as f:
            f.write(image_data)
        
        print(f"\n📊 Graph visualization saved to: {output_file}")
        
        # Try to open it
        subprocess.run(['open', output_file], check=False)
        
    except Exception as e:
        print(f"⚠️  Could not generate graph visualization: {e}")

