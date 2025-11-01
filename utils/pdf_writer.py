"""PDF generation utilities for converting markdown content to PDF"""
import markdown2
import re
import os
from fpdf import FPDF
from urllib.request import urlopen
from io import BytesIO
from PIL import Image
from openai import OpenAI


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


def generate_activity_image(activity_name: str) -> Image.Image:
    """Generate an image for an activity using OpenAI DALL-E.
    
    Args:
        activity_name: Name of the activity to generate image for
        
    Returns:
        PIL Image object or None if generation fails
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(f"⚠️  Warning: OPENAI_API_KEY not found, skipping image generation for {activity_name}")
            return None
        
        client = OpenAI(api_key=api_key)
        
        # Create a descriptive prompt for the activity
        prompt = f"Beautiful, professional travel photography style image of {activity_name}. High quality, vibrant colors, travel brochure aesthetic."
        
        print(f"🖼️  Generating image for: {activity_name}...")
        
        # Generate image using DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download the generated image
        img = download_image(image_url)
        return img
        
    except Exception as e:
        print(f"⚠️  Warning: Could not generate image for {activity_name}: {e}")
        return None


class CustomPDF(PDF):
    """Custom PDF class that handles image insertion and placeholder detection."""
    
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
    
    def add_generated_image(self, img: Image.Image, width_mm: float = 80):
        """Add a generated image (PIL Image) to the PDF.
        
        Args:
            img: PIL Image object
            width_mm: Desired width in millimeters (default 80mm)
        """
        if img is None:
            return False
        
        # Get current position
        x = self.l_margin
        y = self.get_y()
        
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
            print(f"⚠️  Warning: Could not add generated image to PDF: {e}")
            return False


def extract_image_placeholders(markdown_content: str):
    """Extract image placeholders from markdown content.
    
    Args:
        markdown_content: Markdown content with placeholders
        
    Returns:
        List of tuples: (placeholder_text, activity_name, start_pos, end_pos)
    """
    pattern = r'\[IMAGE_PLACEHOLDER:([^\]]+)\]'
    placeholders = []
    
    for match in re.finditer(pattern, markdown_content):
        full_placeholder = match.group(0)
        activity_name = match.group(1)
        start_pos = match.start()
        end_pos = match.end()
        placeholders.append((full_placeholder, activity_name, start_pos, end_pos))
    
    return placeholders


def markdown_to_pdf(markdown_content: str, output_filepath: str) -> None:
    """Convert markdown content to a styled PDF file with image generation.
    
    Args:
        markdown_content: The markdown-formatted text to convert
        output_filepath: Path where the PDF file should be saved
        
    Raises:
        Exception: If PDF generation fails
    """
    try:
        # Extract image placeholders before processing
        placeholders = extract_image_placeholders(markdown_content)
        
        # Generate images for all placeholders (can be done in parallel later)
        placeholder_images = {}
        for placeholder_text, activity_name, start_pos, end_pos in placeholders:
            print(f"📸 Preparing image for: {activity_name}")
            img = generate_activity_image(activity_name)
            if img:
                placeholder_images[placeholder_text] = img
        
        # Create CustomPDF instance
        pdf = CustomPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Split markdown by placeholders to maintain order
        # This approach: split content into segments, interleaved with placeholders
        segments = []
        current_pos = 0
        
        # Sort placeholders by position
        sorted_placeholders = sorted(placeholders, key=lambda x: x[2])
        
        for placeholder_text, activity_name, start_pos, end_pos in sorted_placeholders:
            # Add text segment before this placeholder
            if start_pos > current_pos:
                text_segment = markdown_content[current_pos:start_pos].strip()
                if text_segment:
                    segments.append(('text', text_segment))
            
            # Add placeholder
            segments.append(('image', placeholder_text, activity_name))
            current_pos = end_pos
        
        # Add remaining text after last placeholder
        if current_pos < len(markdown_content):
            text_segment = markdown_content[current_pos:].strip()
            if text_segment:
                segments.append(('text', text_segment))
        
        # If no placeholders found, process entire content as one segment
        if not segments:
            segments.append(('text', markdown_content))
        
        # Process each segment
        for segment in segments:
            if segment[0] == 'text':
                # Convert and write markdown segment
                text_content = segment[1]
                sanitized = sanitize_for_pdf(text_content)
                html_content = markdown2.markdown(
                    sanitized,
                    extras=['fenced-code-blocks', 'tables', 'break-on-newline', 'header-ids', 'code-friendly']
                )
                pdf.write_html(html_content)
            elif segment[0] == 'image':
                # Insert generated image
                placeholder_text = segment[1]
                activity_name = segment[2]
                
                if placeholder_text in placeholder_images:
                    img = placeholder_images[placeholder_text]
                    pdf.add_generated_image(img, width_mm=80)
                    print(f"✅ Image inserted for: {activity_name}")
                else:
                    print(f"⚠️  No image available for: {activity_name}")
        
        # Output PDF
        pdf.output(output_filepath)
        print(f"✅ PDF generated successfully: {output_filepath}")
        
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")
