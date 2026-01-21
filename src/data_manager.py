import logging
import pickle
from pathlib import Path
from typing import Optional

import face_recognition
import numpy as np
from numpy.typing import NDArray

import config
from src.utils import get_person_folders, validate_image_path, sanitize_person_name


class FaceDataManager:
    """Manages face encodings database."""
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.known_face_encodings: list[NDArray[np.float64]] = []
        self.known_face_names: list[str] = []
        self.logger.info("FaceDataManager initialized")
    
    def load_encodings_from_cache(
        self,
        cache_file: Path = config.ENCODINGS_FILE
    ) -> bool:
        """Load encodings from cache file."""
        if not cache_file.exists():
            self.logger.info("No cache file: %s", cache_file)
            return False
        
        try:
            with open(cache_file, "rb") as file:
                data = pickle.load(file)
            
            if not isinstance(data, dict):
                self.logger.warning("Invalid cache format")
                return False
            
            self.known_face_encodings = data.get("encodings", [])
            self.known_face_names = data.get("names", [])
            
            self.logger.info(
                "Cache loaded: %d faces from %s",
                len(self.known_face_encodings),
                cache_file.name
            )
            return True
            
        except Exception as e:
            self.logger.error("Error loading cache: %s", str(e))
            return False
    
    def save_encodings_to_cache(
        self,
        cache_file: Path = config.ENCODINGS_FILE
    ) -> bool:
        """Save encodings to cache file."""
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "encodings": self.known_face_encodings,
                "names": self.known_face_names,
            }
            
            with open(cache_file, "wb") as file:
                pickle.dump(data, file)
            
            self.logger.info(
                "Cache saved: %d faces to %s",
                len(self.known_face_encodings),
                cache_file.name
            )
            return True
            
        except Exception as e:
            self.logger.error("Error saving cache: %s", str(e))
            return False
    
    def build_database_from_images(
        self,
        people_dir: Path = config.PEOPLE_DIR,
        force_rebuild: bool = False
    ) -> int:
        """Build face database from people directory images."""
        if not force_rebuild and self.load_encodings_from_cache():
            return len(self.known_face_encodings)
        
        self.known_face_encodings.clear()
        self.known_face_names.clear()
        
        person_folders = get_person_folders()
        
        if not person_folders:
            self.logger.warning("No person folders found in %s", people_dir)
            return 0
        
        self.logger.info("Building database from %d persons...", len(person_folders))
        
        total_faces = 0
        
        for person_folder in person_folders:
            person_name = sanitize_person_name(person_folder.name)
            self.logger.debug("Processing: %s", person_name)
            
            image_files = [
                img for img in person_folder.iterdir()
                if validate_image_path(img)
            ]
            
            if not image_files:
                self.logger.warning("No images in %s folder", person_folder.name)
                continue
            
            for image_file in image_files:
                faces_count = self._process_image(image_file, person_name)
                total_faces += faces_count
        
        self.logger.info(
            "Database built: %d faces from %d persons",
            total_faces,
            len(set(self.known_face_names))
        )
        
        self.save_encodings_to_cache()
        return total_faces
    
    def _process_image(self, image_path: Path, person_name: str) -> int:
        """Process image and extract face encoding."""
        try:
            image = face_recognition.load_image_file(str(image_path))
            
            face_locations = face_recognition.face_locations(
                image,
                model=config.FACE_DETECTION_MODEL
            )
            
            if not face_locations:
                self.logger.debug("No face found in: %s", image_path.name)
                return 0
            
            face_encodings = face_recognition.face_encodings(
                image,
                known_face_locations=face_locations,
                model=config.ENCODING_MODEL
            )
            
            for encoding in face_encodings:
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(person_name)
            
            self.logger.debug(
                "Processed: %s - %d faces",
                image_path.name,
                len(face_encodings)
            )
            
            return len(face_encodings)
            
        except Exception as e:
            self.logger.error(
                "Error processing %s: %s",
                image_path.name,
                str(e)
            )
            return 0
    
    def get_database_info(self) -> dict[str, int]:
        """Get database statistics."""
        return {
            "total_faces": len(self.known_face_encodings),
            "unique_persons": len(set(self.known_face_names))
        }
    
    def clear_database(self) -> None:
        """Clear all loaded data from memory."""
        self.known_face_encodings.clear()
        self.known_face_names.clear()
        self.logger.info("Database cleared from memory")
