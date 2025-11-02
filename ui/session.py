"""Session state management for Streamlit UI"""
import streamlit as st
from datetime import datetime


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


def reset_session_state():
    """Reset session state for a new trip"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

