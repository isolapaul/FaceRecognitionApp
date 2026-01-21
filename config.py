"""Application configuration - central configuration file."""
from pathlib import Path
from typing import Final

# Project paths
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
PEOPLE_DIR: Final[Path] = DATA_DIR / "people"
ENCODINGS_DIR: Final[Path] = DATA_DIR / "encodings"
LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"
ENCODINGS_FILE: Final[Path] = ENCODINGS_DIR / "face_encodings.pkl"

# Face recognition settings
FACE_MATCH_THRESHOLD: Final[float] = 0.6
FACE_DETECTION_MODEL: Final[str] = "hog"
ENCODING_MODEL: Final[str] = "small"
SUPPORTED_IMAGE_FORMATS: Final[tuple[str, ...]] = (
    ".jpg", ".jpeg", ".png", ".bmp", ".gif"
)

# Logging configuration
LOG_FILE: Final[Path] = LOGS_DIR / "face_recognition.log"
LOG_LEVEL: Final[str] = "INFO"
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

# UI settings
APP_TITLE: Final[str] = "🎭 Face Recognition App"
APP_ICON: Final[str] = "🎭"
MAX_UPLOAD_SIZE_MB: Final[int] = 10


def ensure_directories() -> None:
    """Ensure all required directories exist."""
    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    ENCODINGS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


ensure_directories()
