"""Face recognition engine."""
import logging
from pathlib import Path
from typing import Optional, Union

import face_recognition
import numpy as np
from numpy.typing import NDArray
from PIL import Image

import config
from src.data_manager import FaceDataManager


class FaceRecognizer:
    """Face recognition class."""
    
    def __init__(
        self,
        data_manager: FaceDataManager,
        logger: Optional[logging.Logger] = None,
        match_threshold: float = config.FACE_MATCH_THRESHOLD
    ) -> None:
        self.data_manager = data_manager
        self.logger = logger or logging.getLogger(__name__)
        self.match_threshold = match_threshold
        
        self.logger.info("FaceRecognizer initialized (threshold: %.2f)", self.match_threshold)
    
    def recognize_face(
        self,
        image: Union[str, Path, NDArray[np.uint8], Image.Image]
    ) -> Optional[str]:
        """Recognize a face in the uploaded image."""
        image_array = self._load_and_normalize_image(image)
        
        if image_array is None:
            self.logger.warning("Failed to load image")
            return None
        
        if not self.data_manager.known_face_encodings:
            self.logger.warning("Database is empty!")
            return None
        
        self.logger.debug("Detecting faces...")
        face_locations = face_recognition.face_locations(
            image_array,
            model=config.FACE_DETECTION_MODEL
        )
        
        if not face_locations:
            self.logger.info("No face found in image")
            return None
        
        if len(face_locations) > 1:
            self.logger.warning(
                "Multiple faces found (%d), analyzing first one",
                len(face_locations)
            )
        
        self.logger.debug("Generating encoding...")
        face_encodings = face_recognition.face_encodings(
            image_array,
            known_face_locations=face_locations,
            model=config.ENCODING_MODEL
        )
        
        if not face_encodings:
            self.logger.warning("Failed to generate encoding")
            return None
        
        face_encoding = face_encodings[0]
        recognized_name = self._match_face(face_encoding)
        
        if recognized_name:
            self.logger.info("Face recognized: %s", recognized_name)
        else:
            self.logger.info("Unknown face (no match)")
        
        return recognized_name
    
    def recognize_faces_batch(
        self,
        images: list[Union[str, Path, NDArray[np.uint8], Image.Image]]
    ) -> list[Optional[str]]:
        """Process multiple images in batch."""
        results = []
        self.logger.info("Batch processing: %d images", len(images))
        
        for idx, image in enumerate(images, start=1):
            self.logger.debug("Processing: %d/%d", idx, len(images))
            result = self.recognize_face(image)
            results.append(result)
        
        return results
    
    def _load_and_normalize_image(
        self,
        image: Union[str, Path, NDArray[np.uint8], Image.Image]
    ) -> Optional[NDArray[np.uint8]]:
        """Load and normalize image to face_recognition format."""
        try:
            if isinstance(image, (str, Path)):
                image_path = Path(image)
                
                if not image_path.exists():
                    self.logger.error("Image does not exist: %s", image_path)
                    return None
                
                return face_recognition.load_image_file(str(image_path))
            
            elif isinstance(image, Image.Image):
                return np.array(image.convert("RGB"))
            
            elif isinstance(image, np.ndarray):
                return image
            
            else:
                self.logger.error("Unsupported image format: %s", type(image))
                return None
                
        except Exception as e:
            self.logger.error("Error loading image: %s", str(e))
            return None
    
    def _match_face(self, face_encoding: NDArray[np.float64]) -> Optional[str]:
        """Compare encoding with known faces."""
        face_distances = face_recognition.face_distance(
            self.data_manager.known_face_encodings,
            face_encoding
        )
        
        best_match_index = int(np.argmin(face_distances))
        best_match_distance = face_distances[best_match_index]
        
        self.logger.debug(
            "Best match: %s (distance: %.3f)",
            self.data_manager.known_face_names[best_match_index],
            best_match_distance
        )
        
        if best_match_distance < self.match_threshold:
            return self.data_manager.known_face_names[best_match_index]
        
        return None
    
    def get_detailed_match_results(
        self,
        image: Union[str, Path, NDArray[np.uint8], Image.Image],
        top_n: int = 3
    ) -> list[tuple[str, float]]:
        """Get detailed match results (not just the best one)."""
        image_array = self._load_and_normalize_image(image)
        
        if image_array is None or not self.data_manager.known_face_encodings:
            return []
        
        face_locations = face_recognition.face_locations(
            image_array,
            model=config.FACE_DETECTION_MODEL
        )
        
        if not face_locations:
            return []
        
        face_encodings = face_recognition.face_encodings(
            image_array,
            known_face_locations=face_locations,
            model=config.ENCODING_MODEL
        )
        
        if not face_encodings:
            return []
        
        face_encoding = face_encodings[0]
        face_distances = face_recognition.face_distance(
            self.data_manager.known_face_encodings,
            face_encoding
        )
        
        results = list(zip(self.data_manager.known_face_names, face_distances))
        results.sort(key=lambda x: x[1])
        return results[:top_n]
    
    def recognize_all_faces(
        self,
        image: Union[str, Path, NDArray[np.uint8], Image.Image]
    ) -> list[tuple[str, tuple[int, int, int, int]]]:
        """
        Recognize all faces in an image.
        
        Returns:
            List of tuples: (name, face_location)
            face_location is (top, right, bottom, left)
        """
        image_array = self._load_and_normalize_image(image)
        
        if image_array is None:
            self.logger.warning("Failed to load image")
            return []
        
        if not self.data_manager.known_face_encodings:
            self.logger.warning("Database is empty!")
            return []
        
        self.logger.debug("Detecting all faces...")
        face_locations = face_recognition.face_locations(
            image_array,
            model=config.FACE_DETECTION_MODEL
        )
        
        if not face_locations:
            self.logger.info("No faces found in image")
            return []
        
        self.logger.info("Found %d face(s) in image", len(face_locations))
        
        self.logger.debug("Generating encodings for all faces...")
        face_encodings = face_recognition.face_encodings(
            image_array,
            known_face_locations=face_locations,
            model=config.ENCODING_MODEL
        )
        
        if not face_encodings:
            self.logger.warning("Failed to generate encodings")
            return []
        
        # Match each face
        results = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            recognized_name = self._match_face(face_encoding)
            name = recognized_name if recognized_name else "Ismeretlen"
            results.append((name, face_location))
            self.logger.debug("Face at %s: %s", face_location, name)
        
        return results
