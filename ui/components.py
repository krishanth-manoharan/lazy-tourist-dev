"""Reusable UI components for Streamlit interface"""
import streamlit as st
import streamlit.components.v1 as components
import markdown2
from datetime import datetime


def display_chat_message(role: str, content: str):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{content}</div>', unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f'<div class="chat-message assistant-message"><strong>🤖 AI Assistant:</strong><br>{content}</div>', unsafe_allow_html=True)
    elif role == "system":
        st.markdown(f'<div class="chat-message system-message">{content}</div>', unsafe_allow_html=True)


def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🌍 Lazy Tourist - AI Travel Planner</h1>
        <p>Your Personal AI Travel Planning Assistant</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_usage_guide():
    """Render the usage guide in sidebar"""
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Describe your dream trip** in the chat
    2. **Review** the generated itinerary
    3. **Request changes** and refinements
    4. **Save** when you're happy!
    """)


def render_example_queries():
    """Render example queries in sidebar"""
    st.markdown("### 💡 Example Queries")
    
    example_queries = [
        "Plan a 5-day trip to Paris from NYC for 2, budget $3000, love food",
        "4-day NYC to Bali getaway for 2 people, budget $2500, love beaches",
        "One week NYC-Tokyo trip for family of 3, budget $5000",
        "Cheap 3-day Paris trip for 1 person, $1000 budget"
    ]
    
    for i, query in enumerate(example_queries):
        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(query, key=f"example_{i}", use_container_width=True):
                st.session_state.user_input = query
                st.rerun()
        with col2:
            # Copy button using HTML component
            escaped_query = query.replace("'", "\\'")
            copy_button_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        background-color: transparent;
                    }}
                </style>
            </head>
            <body>
            <div style="height: 38px; display: flex; align-items: center;">
                <button 
                    onclick="
                        navigator.clipboard.writeText('{escaped_query}');
                        this.innerHTML = '✅';
                        setTimeout(() => {{ this.innerHTML = '📋'; }}, 1500);
                    "
                    style="
                        width: 100%;
                        height: 100%;
                        background-color: #2d3139;
                        color: white;
                        border: 1px solid #667eea;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 1.2rem;
                        transition: all 0.3s ease;
                    "
                    onmouseover="this.style.backgroundColor='#667eea'"
                    onmouseout="this.style.backgroundColor='#2d3139'"
                >📋</button>
            </div>
            </body>
            </html>
            """
            components.html(copy_button_html, height=38)


def render_trip_info():
    """Render current trip information in sidebar"""
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


def render_sidebar_about():
    """Render about section in sidebar"""
    st.markdown("### ℹ️ About")
    st.markdown("""
    Built with **LangGraph** and **GPT-4o-mini** for intelligent, 
    conversational travel planning.
    
    Say "save" or "perfect" when satisfied!
    """)


def render_itinerary_view():
    """Render the itinerary in main view"""
    st.markdown("### ✈️ Your Itinerary")
    
    # Create a container with custom CSS class for styling
    itinerary_container = st.container()
    with itinerary_container:
        # Convert markdown to HTML for proper rendering
        itinerary_html = markdown2.markdown(st.session_state.current_itinerary)
        st.markdown(f"""
        <div class="itinerary-main">
            <div class="itinerary-box">
                {itinerary_html}
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


def render_chat_panel(in_sidebar: bool = False):
    """
    Render chat panel with messages and input
    
    Args:
        in_sidebar: Whether this is rendered in sidebar layout (compact) or main layout
    """
    from ui.handlers import process_user_input
    
    if in_sidebar:
        # Compact chat panel header for sidebar layout
        st.markdown('<div class="chat-panel-header">💬 Chat</div>', unsafe_allow_html=True)
        chat_height = 500
    else:
        # Full chat header for main layout
        st.markdown("### 💬 Chat with Your Travel Assistant")
        chat_height = None
    
    # Chat messages container
    if chat_height:
        chat_container = st.container(height=chat_height)
    else:
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
                input_placeholder = "Request changes or say 'save'" if in_sidebar else "Ask questions, request changes, or say 'save' when satisfied"
                user_input = st.text_input(
                    "Your message:",
                    placeholder=input_placeholder,
                    key="user_input_field",
                    label_visibility="collapsed" if in_sidebar else "visible"
                )
                submit_label = "Send"
            
            submit = st.form_submit_button(submit_label, use_container_width=True)
            
            if submit and user_input:
                process_user_input(user_input)
                st.rerun()
    else:
        if in_sidebar:
            st.success("🎉 Complete!")
            st.info("Start a new trip from the sidebar!")
        else:
            st.success("🎉 Trip planning complete! Check the outputs folder for your saved itinerary.")
            st.info("Click '🔄 Start New Trip' in the sidebar to plan another adventure!")

