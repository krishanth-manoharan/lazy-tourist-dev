"""CSS styles for Streamlit UI"""

DARK_THEME_CSS = """
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
"""

