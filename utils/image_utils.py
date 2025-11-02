"""Image processing utilities for visualization and theming"""
import io
from typing import Optional


def invert_image_colors(image_data: bytes) -> Optional[bytes]:
    """Invert image colors for dark theme visualization
    
    Args:
        image_data: Original image data in bytes (PNG format)
        
    Returns:
        Inverted image data in bytes, or None if Pillow is not available
        
    Raises:
        ImportError: If PIL/Pillow is not installed
    """
    try:
        from PIL import Image, ImageOps
        
        # Load image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Invert colors for dark mode effect
        img_inverted = ImageOps.invert(img)
        
        # Save back to bytes
        output_buffer = io.BytesIO()
        img_inverted.save(output_buffer, format='PNG')
        
        return output_buffer.getvalue()
        
    except ImportError as e:
        raise ImportError(
            "PIL/Pillow is required for dark mode visualization. "
            "Install it with: pip install Pillow"
        ) from e


def convert_to_dark_theme(image_data: bytes, fallback_on_error: bool = True) -> tuple[bytes, bool]:
    """Convert an image to dark theme by inverting colors
    
    Args:
        image_data: Original image data in bytes
        fallback_on_error: If True, return original image if conversion fails
        
    Returns:
        Tuple of (image_data, success_flag):
        - image_data: Inverted image if successful, original if fallback enabled
        - success_flag: True if conversion succeeded, False otherwise
    """
    try:
        inverted_data = invert_image_colors(image_data)
        return inverted_data, True
    except ImportError:
        if fallback_on_error:
            return image_data, False
        raise
    except Exception:
        if fallback_on_error:
            return image_data, False
        raise

