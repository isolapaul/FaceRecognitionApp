"""Utility functions."""
import logging
from pathlib import Path
from typing import Optional, cast

from PIL import Image, ImageOps, ImageDraw, ImageFont

import config


def setup_logging(
    log_level: str = config.LOG_LEVEL,
    log_file: Optional[Path] = config.LOG_FILE
) -> logging.Logger:
    """Configure application logging."""
    logger = logging.getLogger("FaceRecognitionApp")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.info("Logging initialized at %s level", log_level)
    return logger


def validate_image_path(image_path: Path) -> bool:
    """Check if image file is valid and supported."""
    if not image_path.exists():
        return False
    
    if not image_path.is_file():
        return False
    
    if image_path.suffix.lower() not in config.SUPPORTED_IMAGE_FORMATS:
        return False
    
    return True


def sanitize_person_name(folder_name: str) -> str:
    """Convert folder name to readable person name."""
    name = folder_name.replace("_", " ")
    name = name.title()
    return name


def fix_image_orientation(image: Image.Image) -> Image.Image:
    """Fix image orientation based on EXIF data."""
    try:
        # Use ImageOps.exif_transpose to handle EXIF orientation
        result = ImageOps.exif_transpose(image)
        return cast(Image.Image, result) if result is not None else image
    except Exception:
        # If no EXIF data or error, return original
        return image


def draw_face_annotations(
    image: Image.Image,
    recognized_faces: list[tuple[str, tuple[int, int, int, int]]]
) -> Image.Image:
    """
    Draw colored rectangles, arrows and names for recognized faces.
    
    Args:
        image: PIL Image
        recognized_faces: List of (name, (top, right, bottom, left))
    
    Returns:
        Annotated PIL Image
    """
    # Color palette (6 colors cycle)
    colors = [
        (0, 255, 0),      # Green
        (0, 0, 255),      # Blue
        (255, 105, 180),  # Pink
        (255, 215, 0),    # Gold
        (255, 0, 0),      # Red
        (138, 43, 226)    # Purple
    ]
    
    img_copy = cast(Image.Image, image.copy())
    draw = ImageDraw.Draw(img_copy)
    
    # Try to load a font, fall back to default if not available
    font_size = 0  # Initialize before try block
    try:
        font_size = max(20, min(img_copy.height, img_copy.width) // 30)
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
        font_size = 10
    
    for idx, (name, face_location) in enumerate(recognized_faces):
        top, right, bottom, left = face_location
        color = colors[idx % len(colors)]
        
        # Draw rectangle around face (3px thick)
        for offset in range(3):
            draw.rectangle(
                [(left - offset, top - offset), (right + offset, bottom + offset)],
                outline=color
            )
        
        # Calculate arrow position (from right side of face)
        arrow_start_x = right + 10
        arrow_start_y = (top + bottom) // 2
        arrow_end_x = arrow_start_x + 50
        arrow_end_y = arrow_start_y
        
        # Draw arrow line
        draw.line(
            [(arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y)],
            fill=color,
            width=2
        )
        
        # Draw arrow head
        arrow_size = 8
        draw.polygon(
            [
                (arrow_end_x, arrow_end_y),
                (arrow_end_x - arrow_size, arrow_end_y - arrow_size),
                (arrow_end_x - arrow_size, arrow_end_y + arrow_size)
            ],
            fill=color
        )
        
        # Draw name with black background
        text_x = arrow_end_x + 10
        text_y = arrow_end_y - font_size // 2
        
        # Get text bounding box
        bbox = draw.textbbox((text_x, text_y), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Draw black background rectangle
        padding = 4
        draw.rectangle(
            [
                (text_x - padding, text_y - padding),
                (text_x + text_width + padding, text_y + text_height + padding)
            ],
            fill=(0, 0, 0)
        )
        
        # Draw text
        draw.text((text_x, text_y), name, fill=color, font=font)
    
    return img_copy
