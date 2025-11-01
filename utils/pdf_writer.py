"""PDF generation utilities for converting markdown content to PDF"""
import markdown2
import re
from fpdf import FPDF
from urllib.request import urlopen
from io import BytesIO
from PIL import Image


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


def extract_images_from_html(html_content: str):
    """Extract image tags from HTML and return list of image info.
    
    Args:
        html_content: HTML content with img tags
        
    Returns:
        List of dicts with keys: 'src', 'alt', 'width', 'original_tag'
    """
    images = []
    # Pattern to match img tags with various attribute orders
    img_pattern = r'<img\s+([^>]*?)>'
    
    def process_img_tag(match):
        attrs_str = match.group(1)
        original_tag = match.group(0)
        
        # Extract src
        src_match = re.search(r'src=["\']([^"\']*)["\']', attrs_str, re.IGNORECASE)
        src = src_match.group(1) if src_match else None
        
        # Extract alt
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', attrs_str, re.IGNORECASE)
        alt = alt_match.group(1) if alt_match else ''
        
        # Extract width attribute
        width_match = re.search(r'width=["\'](\d+(?:\.\d+)?)\s*(mm|px|pt|in|cm)?["\']', attrs_str, re.IGNORECASE)
        width_value = None
        width_unit = 'mm'
        
        if width_match:
            width_value = float(width_match.group(1))
            if width_match.group(2):
                width_unit = width_match.group(2).lower()
        
        if src:
            images.append({
                'src': src,
                'alt': alt,
                'width': width_value,
                'width_unit': width_unit,
                'original_tag': original_tag
            })
            # Replace with placeholder that we'll use for positioning
            return f'[IMAGE_PLACEHOLDER_{len(images)-1}]'
        
        return original_tag
    
    # Replace img tags with placeholders
    processed_html = re.sub(img_pattern, process_img_tag, html_content, flags=re.IGNORECASE)
    
    return processed_html, images


def download_image(url: str):
    """Download image from URL and return PIL Image object.
    
    Args:
        url: Image URL
        
    Returns:
        PIL Image object or None if download fails
    """
    try:
        response = urlopen(url, timeout=10)
        img_data = response.read()
        img = Image.open(BytesIO(img_data))
        return img
    except Exception as e:
        print(f"⚠️  Warning: Could not download image from {url}: {e}")
        return None


def convert_width_to_mm(width_value: float, unit: str) -> float:
    """Convert width from various units to millimeters.
    
    Args:
        width_value: The width value
        unit: Unit (mm, px, pt, in, cm)
        
    Returns:
        Width in millimeters
    """
    unit = unit.lower()
    if unit == 'mm' or unit == '':
        return width_value
    elif unit == 'cm':
        return width_value * 10
    elif unit == 'in':
        return width_value * 25.4
    elif unit == 'px':
        # Approximate: 1mm ≈ 3.7795px at 96 DPI
        return width_value / 3.7795
    elif unit == 'pt':
        # 1mm ≈ 2.83465pt
        return width_value / 2.83465
    else:
        return width_value  # Default to assuming mm


class CustomPDF(PDF):
    """Custom PDF class that handles image insertion."""
    
    def add_image_from_url(self, url: str, width_mm: float = None, alt: str = ''):
        """Add image from URL with specified width.
        
        Args:
            url: Image URL
            width_mm: Desired width in millimeters (None to use default 80mm)
            alt: Alt text for image
        """
        img = download_image(url)
        if img is None:
            return False
        
        # Get current position
        x = self.l_margin
        y = self.get_y()
        
        # Default width if not specified
        if width_mm is None:
            width_mm = 50
        
        # Calculate height maintaining aspect ratio
        img_width_px, img_height_px = img.size
        aspect_ratio = img_height_px / img_width_px
        height_mm = width_mm * aspect_ratio
        
        # Check if image fits on current page
        if y + height_mm > self.page_break_trigger:
            self.add_page()
            y = self.t_margin
        
        try:
            # Save image to temporary bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Add image to PDF
            self.image(img_bytes, x=x, y=y, w=width_mm, h=height_mm)
            
            # Move Y position after image
            self.set_y(y + height_mm + 5)  # 5mm spacing after image
            
            return True
        except Exception as e:
            print(f"⚠️  Warning: Could not add image to PDF: {e}")
            return False


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
        # print("Sanitized content: ", sanitized_content)
        
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

        # Extract images from HTML
        html_without_images, images = extract_images_from_html(html_content)
        
        print("HTML content: ", html_content)
        print(f"Extracted {len(images)} images")
        
        # Create PDF instance with custom image handling
        pdf = CustomPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # If no images, just write HTML normally
        if len(images) == 0:
            pdf.write_html(html_content)
        else:
            # Split HTML by image placeholders and process in segments
            segments = html_without_images.split('[IMAGE_PLACEHOLDER_')
            
            for i, segment in enumerate(segments):
                if i == 0:
                    # First segment - write normally
                    if segment.strip():
                        pdf.write_html(segment)
                else:
                    # Segment contains image placeholder
                    parts = segment.split(']', 1)
                    img_index = int(parts[0]) if parts[0].isdigit() else None
                    remaining_html = parts[1] if len(parts) > 1 else ''
                    
                    # Insert image if valid index
                    if img_index is not None and img_index < len(images):
                        img_info = images[img_index]
                        width_mm = None
                        if img_info['width'] is not None:
                            width_mm = convert_width_to_mm(img_info['width'], img_info['width_unit'])
                        
                        pdf.add_image_from_url(img_info['src'], width_mm=width_mm, alt=img_info['alt'])
                    
                    # Write remaining HTML after image
                    if remaining_html.strip():
                        pdf.write_html(remaining_html)
        
        # Output PDF
        pdf.output(output_filepath)
        
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")
