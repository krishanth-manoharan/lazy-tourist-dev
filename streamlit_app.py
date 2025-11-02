"""Streamlit UI for Lazy Tourist Travel Planning Agent"""
import streamlit as st
from dotenv import load_dotenv
from graph import create_travel_agent_graph
from agents.state import TravelState
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Lazy Tourist - AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark Theme
st.markdown("""
<style>
    /* Global dark theme */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #0e1117;
    }
    
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }
    
    .user-message {
        background-color: #1e3a5f;
        border-left: 4px solid #4a9eff;
        color: #e3f2fd;
    }
    
    .assistant-message {
        background-color: #2d1b3d;
        border-left: 4px solid #b388ff;
        color: #e1bee7;
    }
    
    .system-message {
        background-color: #2d2416;
        border-left: 4px solid #ffb74d;
        font-style: italic;
        color: #ffe0b2;
    }
    
    .itinerary-box {
        background-color: #1a1d24;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #667eea;
        margin: 1rem 0;
        color: #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .itinerary-box h1, .itinerary-box h2, .itinerary-box h3 {
        color: #b388ff;
    }
    
    .itinerary-box strong {
        color: #4a9eff;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #764ba2;
        box-shadow: 0 4px 8px rgba(102,126,234,0.4);
        transform: translateY(-2px);
    }
    
    .sidebar-info {
        padding: 1rem;
        background-color: #1a1d24;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #2d3139;
        color: #e0e0e0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #161b22;
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #1a1d24;
        color: #fafafa;
        border: 1px solid #2d3139;
        border-radius: 8px;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 1px #667eea;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #2ea043;
        color: white;
        border-radius: 8px;
        border: none;
    }
    
    .stDownloadButton>button:hover {
        background-color: #26843b;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #1a1d24;
        border: 1px solid #2d3139;
        color: #e0e0e0;
    }
    
    /* Itinerary main view */
    .itinerary-main {
        background-color: #0e1117;
        padding: 1.5rem;
        border-radius: 12px;
        overflow-y: auto;
    }
    
    .chat-panel-header {
        color: #b388ff;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding: 0.75rem;
        background-color: #1a1d24;
        border-radius: 8px;
        border-bottom: 2px solid #2d3139;
    }
    
    /* Streamlit container styling for chat */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background-color: #161b22;
        border-radius: 8px;
    }
    
    /* Scrollbar styling for dark theme */
    .itinerary-main::-webkit-scrollbar,
    [data-testid="stVerticalBlock"]::-webkit-scrollbar {
        width: 8px;
    }
    
    .itinerary-main::-webkit-scrollbar-track,
    [data-testid="stVerticalBlock"]::-webkit-scrollbar-track {
        background: #1a1d24;
        border-radius: 4px;
    }
    
    .itinerary-main::-webkit-scrollbar-thumb,
    [data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 4px;
    }
    
    .itinerary-main::-webkit-scrollbar-thumb:hover,
    [data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.chat_history = []
        st.session_state.app = None
        st.session_state.thread_config = {"configurable": {"thread_id": f"streamlit_session_{datetime.now().timestamp()}"}}
        st.session_state.state = None
        st.session_state.is_first_run = True
        st.session_state.pending_state_update = None
        st.session_state.iteration_count = 0
        st.session_state.planning_started = False
        st.session_state.planning_complete = False
        st.session_state.awaiting_input = False
        st.session_state.current_itinerary = ""
        st.session_state.trip_info = {}

def display_chat_message(role: str, content: str):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{content}</div>', unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f'<div class="chat-message assistant-message"><strong>🤖 AI Assistant:</strong><br>{content}</div>', unsafe_allow_html=True)
    elif role == "system":
        st.markdown(f'<div class="chat-message system-message">{content}</div>', unsafe_allow_html=True)

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
                                    "content": "📄 Your itinerary is ready! Review it and provide feedback."
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

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 Lazy Tourist - AI Travel Planner</h1>
        <p>Your Personal AI Travel Planning Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. **Describe your dream trip** in the chat
        2. **Review** the generated itinerary
        3. **Request changes** and refinements
        4. **Save** when you're happy!
        """)
        
        st.markdown("---")
        
        st.markdown("### 💡 Example Queries")
        example_queries = [
            "Plan a 5-day trip to Paris for 2, budget $3000, love food",
            "4-day Bali getaway for 2 people, budget $2500, love beaches",
            "One week Tokyo trip for family of 3, budget $5000",
            "Cheap 3-day Paris trip for 1 person, $1000 budget"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}"):
                st.session_state.user_input = query
                st.rerun()
        
        st.markdown("---")
        
        # Trip info
        if st.session_state.trip_info:
            st.markdown("### 🎯 Current Trip")
            st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
            
            if st.session_state.trip_info.get("destination"):
                st.markdown(f"**📍 Destination:** {st.session_state.trip_info.get('destination', 'N/A')}")
            if st.session_state.trip_info.get("duration_days"):
                st.markdown(f"**📅 Duration:** {st.session_state.trip_info.get('duration_days', 'N/A')} days")
            if st.session_state.trip_info.get("budget"):
                st.markdown(f"**💰 Budget:** ${st.session_state.trip_info.get('budget', 'N/A')}")
            if st.session_state.trip_info.get("num_adults"):
                adults = st.session_state.trip_info.get('num_adults', 0)
                children = st.session_state.trip_info.get('num_children', 0)
                st.markdown(f"**👥 Travelers:** {adults} adults, {children} children")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Start New Trip", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        Built with **LangGraph** and **GPT-4o-mini** for intelligent, 
        conversational travel planning.
        
        Say "save" or "perfect" when satisfied!
        """)
    
    # Layout changes based on whether itinerary exists
    if st.session_state.current_itinerary:
        # Two-column layout: Itinerary (left/main) + Chat (right/sidebar-like)
        col_itinerary, col_chat = st.columns([2.5, 1])
        
        # Left column: Itinerary (main focus)
        with col_itinerary:
            st.markdown("### 📄 Your Itinerary")
            
            # Create a container with custom CSS class for styling
            itinerary_container = st.container()
            with itinerary_container:
                st.markdown(f"""
                <div class="itinerary-main">
                    <div class="itinerary-box">
                        {st.session_state.current_itinerary}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Download button
            destination = st.session_state.trip_info.get("destination", "trip")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"itinerary_{destination}_{timestamp}.md"
            
            st.download_button(
                label="📥 Download Itinerary",
                data=st.session_state.current_itinerary,
                file_name=filename,
                mime="text/markdown",
                key="download_btn"
            )
        
        # Right column: Chat panel (compact, like copilot)
        with col_chat:
            # Chat header
            st.markdown('<div class="chat-panel-header">💬 Chat</div>', unsafe_allow_html=True)
            
            # Chat messages container
            chat_container = st.container(height=500)
            with chat_container:
                for msg in st.session_state.chat_history:
                    display_chat_message(msg["role"], msg["content"])
            
            # Input area
            if not st.session_state.planning_complete:
                with st.form(key="chat_form", clear_on_submit=True):
                    user_input = st.text_input(
                        "Your message:",
                        placeholder="Request changes or say 'save'",
                        key="user_input_field",
                        label_visibility="collapsed"
                    )
                    submit = st.form_submit_button("Send", use_container_width=True)
                    
                    if submit and user_input:
                        process_user_input(user_input)
                        st.rerun()
            else:
                st.success("🎉 Complete!")
                st.info("Start a new trip from the sidebar!")
    
    else:
        # Initial single-column layout for first interaction
        st.markdown("### 💬 Chat with Your Travel Assistant")
        
        # Chat history
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                display_chat_message(msg["role"], msg["content"])
        
        # Input area
        if not st.session_state.planning_complete:
            with st.form(key="chat_form", clear_on_submit=True):
                if not st.session_state.planning_started:
                    user_input = st.text_area(
                        "✈️ Describe your dream trip:",
                        placeholder="Example: Plan a 5-day trip to Paris for 2 adults, budget $3000, love food and history",
                        height=100,
                        key="user_input_area"
                    )
                    submit_label = "🚀 Start Planning"
                else:
                    user_input = st.text_input(
                        "Your message:",
                        placeholder="Ask questions, request changes, or say 'save' when satisfied",
                        key="user_input_field"
                    )
                    submit_label = "Send"
                
                submit = st.form_submit_button(submit_label)
                
                if submit and user_input:
                    process_user_input(user_input)
                    st.rerun()
        else:
            st.success("🎉 Trip planning complete! Check the outputs folder for your saved itinerary.")
            st.info("Click '🔄 Start New Trip' in the sidebar to plan another adventure!")

if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OpenAI API key not found! Please set OPENAI_API_KEY in your .env file.")
        st.stop()
    
    main()

