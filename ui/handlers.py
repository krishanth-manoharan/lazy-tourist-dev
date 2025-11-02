"""Event handlers and processing logic for Streamlit UI"""
import streamlit as st
from graph import create_travel_agent_graph


def process_user_input(user_input: str):
    """Process user input and run the agent"""
    if not user_input.strip():
        return
    
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Create the agent graph if not already created
    if st.session_state.app is None:
        with st.spinner("🔧 Initializing travel planning system..."):
            st.session_state.app = create_travel_agent_graph()
            st.session_state.chat_history.append({
                "role": "system",
                "content": "✅ Travel planning system initialized!"
            })
    
    # Initialize state for first run
    if st.session_state.is_first_run:
        st.session_state.state = {
            "messages": [],
            "user_query": user_input,
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
            "conversation_history": [f"User: {user_input}"],
            "show_itinerary": True,
            "assistant_response": "",
            "user_feedback_input": ""
        }
        st.session_state.is_first_run = False
        st.session_state.planning_started = True
        stream_input = st.session_state.state
    else:
        # Update state with user feedback - CRITICAL: Set actual user input FIRST
        if st.session_state.pending_state_update:
            # Always update conversation history with user input
            conversation_history = st.session_state.pending_state_update.get("conversation_history", [])
            if f"User: {user_input}" not in conversation_history:
                conversation_history.append(f"User: {user_input}")
            st.session_state.pending_state_update["conversation_history"] = conversation_history
            
            # If this is feedback input, update it with the actual user's message
            if "user_feedback_input" in st.session_state.pending_state_update:
                st.session_state.pending_state_update["user_feedback_input"] = user_input
            
            # Now update the state with the corrected pending update
            st.session_state.app.update_state(
                st.session_state.thread_config,
                st.session_state.pending_state_update,
                as_node="get_feedback" if "user_feedback_input" in st.session_state.pending_state_update else "extract_intent"
            )
        stream_input = None
    
    # Run the agent
    st.session_state.iteration_count += 1
    st.session_state.awaiting_input = False
    state_update = None
    
    progress_placeholder = st.empty()
    
    try:
        # Stream the graph execution
        for step_output in st.session_state.app.stream(stream_input, st.session_state.thread_config, stream_mode="updates"):
            if isinstance(step_output, dict):
                for node_name, node_state in step_output.items():
                    # Update progress
                    progress_placeholder.info(f"🔄 Processing: {node_name.replace('_', ' ').title()}...")
                    
                    # Handle nodes that need user input
                    if node_name == "extract_intent":
                        if node_state.get("needs_user_input"):
                            feedback_msg = node_state.get("feedback_message", "")
                            if feedback_msg:
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": feedback_msg
                                })
                            
                            # Update conversation history
                            conversation_history = node_state.get("conversation_history", [])
                            conversation_history.append(f"Assistant: {feedback_msg}")
                            
                            state_update = {
                                "conversation_history": conversation_history,
                                "needs_user_input": False
                            }
                            st.session_state.awaiting_input = True
                            break
                    
                    elif node_name == "get_feedback":
                        if node_state.get("needs_user_input"):
                            # Check if we should show itinerary
                            show_itinerary = node_state.get("show_itinerary", True)
                            
                            if show_itinerary and node_state.get("final_itinerary"):
                                # Update itinerary
                                st.session_state.current_itinerary = node_state.get("final_itinerary", "")
                                # Add a system message to chat indicating itinerary is ready
                                st.session_state.chat_history.append({
                                    "role": "system",
                                    "content": "📜 Your itinerary is ready! Review it and provide feedback."
                                })
                            
                            # Display assistant response if exists (for clarification questions)
                            assistant_response = node_state.get("assistant_response", "")
                            if assistant_response and not show_itinerary:
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": assistant_response
                                })
                            
                            state_update = {
                                "user_feedback_input": "",
                                "needs_user_input": False,
                                "show_itinerary": True  # Reset for next iteration
                            }
                            st.session_state.awaiting_input = True
                            break
                    
                    # Update trip info for sidebar
                    if node_name == "extract_intent" and node_state.get("preferences"):
                        st.session_state.trip_info = node_state.get("preferences", {})
                    
                    # Save final itinerary
                    if node_name == "save_and_exit":
                        st.session_state.planning_complete = True
                        st.session_state.awaiting_input = False
                        st.session_state.chat_history.append({
                            "role": "system",
                            "content": "🎉 Your trip is all set! Your itinerary has been saved to the outputs folder."
                        })
                
                if st.session_state.awaiting_input:
                    break
        
        progress_placeholder.empty()
        
        # Save state update for next iteration (user input will be added in next call)
        if state_update:
            st.session_state.pending_state_update = state_update
        
        # If we're not waiting for input and not complete, something went wrong
        if not st.session_state.awaiting_input and not st.session_state.planning_complete:
            st.session_state.chat_history.append({
                "role": "system",
                "content": "✅ Planning complete!"
            })
            st.session_state.planning_complete = True
    
    except Exception as e:
        progress_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")
        st.session_state.chat_history.append({
            "role": "system",
            "content": f"❌ An error occurred: {str(e)}"
        })
        st.session_state.awaiting_input = False

