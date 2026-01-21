"""Utility functions."""
import logging
from pathlib import Path
from typing import Optional

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


def get_person_folders() -> list[Path]:
    """Get all person folders from people directory."""
    people_dir = config.PEOPLE_DIR
    
    if not people_dir.exists():
        return []
    
    return [
        folder for folder in people_dir.iterdir()
        if folder.is_dir() and not folder.name.startswith(".")
    ]


def sanitize_person_name(folder_name: str) -> str:
    """Convert folder name to readable person name."""
    name = folder_name.replace("_", " ")
    name = name.title()
    return name
