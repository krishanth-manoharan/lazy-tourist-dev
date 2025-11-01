"""PDF generation utilities for converting markdown content to PDF"""
import markdown2
import re
from fpdf import FPDF


class PDF(FPDF):
    """Custom PDF class with header/footer"""
    
    def header(self):
        """Add header to each page"""
        pass
    
    def footer(self):
        """Add footer with page number"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def sanitize_for_pdf(text: str) -> str:
    """Remove or replace characters that can't be rendered in PDF.
    
    Args:
        text: The text to sanitize
        
    Returns:
        Sanitized text safe for PDF rendering
    """
    # Common emoji replacements
    emoji_map = {
        '🌍': '[Globe]',
        '✈️': '[Flight]',
        '🏨': '[Hotel]',
        '🍽️': '[Restaurant]',
        '🎭': '[Theater]',
        '🏛️': '[Museum]',
        '🎨': '[Art]',
        '🎪': '[Entertainment]',
        '⭐': '*',
        '✅': '[✓]',
        '❌': '[X]',
        '💰': '$',
        '📍': '[Pin]',
        '🗺️': '[Map]',
        '📅': '[Calendar]',
        '⏰': '[Time]',
        '🚗': '[Car]',
        '🚕': '[Taxi]',
        '🚌': '[Bus]',
        '🚂': '[Train]',
        '⚡': '[!]',
        '💡': '[Tip]',
        '📝': '[Note]',
        '🎉': '[Celebration]',
        '🌟': '*',
        '❤️': '<3',
        '🔥': '[Hot]',
        '💎': '[Gem]',
        '🏆': '[Trophy]',
    }
    
    # Replace known emojis
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
    
    # Remove any remaining emojis and special Unicode characters
    # Keep only printable ASCII and common extended Latin characters
    text = re.sub(r'[^\x20-\x7E\xA0-\xFF\n\r\t]', '', text)
    
    return text


def markdown_to_pdf(markdown_content: str, output_filepath: str) -> None:
    """Convert markdown content to a styled PDF file.
    
    Args:
        markdown_content: The markdown-formatted text to convert
        output_filepath: Path where the PDF file should be saved
        
    Raises:
        Exception: If PDF generation fails
    """
    try:
        # Sanitize content to remove emojis and unsupported characters
        sanitized_content = sanitize_for_pdf(markdown_content)
        
        # Convert markdown to HTML with extras
        html_content = markdown2.markdown(
            sanitized_content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'break-on-newline',
                'header-ids',
                'code-friendly'
            ]
        )
        
        # Create PDF instance
        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Write HTML content to PDF
        pdf.write_html(html_content)
        
        # Output PDF
        pdf.output(output_filepath)
        
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")
