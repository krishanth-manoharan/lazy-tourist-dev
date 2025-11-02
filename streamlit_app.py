"""Streamlit UI for Lazy Tourist Travel Planning Agent"""
import streamlit as st
import os
from dotenv import load_dotenv

from ui.styles import DARK_THEME_CSS
from ui.session import initialize_session_state, reset_session_state
from ui.components import (
    render_header,
    render_sidebar_usage_guide,
    render_example_queries,
    render_trip_info,
    render_sidebar_about,
    render_itinerary_view,
    render_chat_panel
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Lazy Tourist - AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with all components"""
    with st.sidebar:
        render_sidebar_usage_guide()
        st.markdown("---")
        render_example_queries()
        st.markdown("---")
        render_trip_info()
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Start New Trip", type="primary"):
            reset_session_state()
            st.rerun()
        
        st.markdown("---")
        render_sidebar_about()


def render_main_content():
    """Render the main content area based on application state"""
    if st.session_state.current_itinerary:
        # Two-column layout: Itinerary (left/main) + Chat (right/sidebar-like)
        col_itinerary, col_chat = st.columns([2.5, 1])
        
        # Left column: Itinerary (main focus)
        with col_itinerary:
            render_itinerary_view()
        
        # Right column: Chat panel (compact)
        with col_chat:
            render_chat_panel(in_sidebar=True)
    else:
        # Initial single-column layout for first interaction
        render_chat_panel(in_sidebar=False)


def main():
    """Main Streamlit application"""
    initialize_session_state()
    render_header()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OpenAI API key not found! Please set OPENAI_API_KEY in your .env file.")
        st.stop()
    
    main()
