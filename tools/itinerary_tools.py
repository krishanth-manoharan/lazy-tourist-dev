"""Itinerary management tools for updating and saving itineraries"""
from langchain_core.tools import tool
import os
from datetime import datetime
import re
from utils.pdf_writer import markdown_to_pdf

# Global variable to store current itinerary content
current_itinerary_content = ""

@tool
def update_itinerary_content(content: str) -> str:
    """Update the current itinerary content with new or modified information.
    
    Args:
        content: The complete updated itinerary content in markdown format
    
    Returns:
        Confirmation message with preview of updated content
    """
    global current_itinerary_content
    current_itinerary_content = content
    
    # Return a preview
    lines = content.split('\n')
    preview = '\n'.join(lines[:10]) + '\n...(content updated)'
    
    return f"✅ Itinerary content updated!\n\nPreview:\n{preview}"

@tool
def save_itinerary_to_file(filename: str, destination: str = "trip") -> str:
    """Save the current itinerary content to a PDF file in the outputs directory.
    
    Args:
        filename: Optional custom filename (without extension)
        destination: Destination name for the filename
    
    Returns:
        Path to the saved file
    """
    global current_itinerary_content
    
    # Create outputs directory if it doesn't exist
    outputs_dir = "outputs"
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    
    # Create safe filename
    if not filename:
        safe_destination = re.sub(r'[^\w\s-]', '', destination).strip().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"itinerary_{safe_destination}_{timestamp}"
    
    # Ensure .pdf extension
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    # Full path
    filepath = os.path.join(outputs_dir, filename)
    
    # Save the file as PDF
    try:
        # Use the PDF writer utility to convert markdown to PDF
        markdown_to_pdf(current_itinerary_content, filepath)
        return f"✅ Itinerary saved successfully to: {filepath}"
    except Exception as e:
        return f"❌ Error saving itinerary: {str(e)}"

@tool
def get_current_itinerary() -> str:
    """Get the current itinerary content.
    
    Returns:
        The current itinerary content
    """
    global current_itinerary_content
    if not current_itinerary_content:
        return "No itinerary content available yet."
    return current_itinerary_content

def set_itinerary_content(content: str):
    """Helper function to set itinerary content (not a tool, used internally)"""
    global current_itinerary_content
    current_itinerary_content = content

def get_itinerary_content() -> str:
    """Helper function to get itinerary content (not a tool, used internally)"""
    global current_itinerary_content
    return current_itinerary_content

