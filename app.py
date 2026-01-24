"""Face Recognition Streamlit Application."""
import logging
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image

import config
from src.data_manager import FaceDataManager
from src.face_engine import FaceRecognizer
from src.utils import setup_logging, fix_image_orientation, draw_face_annotations


st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def get_logger() -> logging.Logger:
    """Create and cache logger."""
    return setup_logging()


logger = get_logger()


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "awaiting_confirmation" not in st.session_state:
        st.session_state.awaiting_confirmation = False
    if "recognized_faces" not in st.session_state:
        st.session_state.recognized_faces = []
    if "current_image" not in st.session_state:
        st.session_state.current_image = None
    if "current_filename" not in st.session_state:
        st.session_state.current_filename = None


@st.cache_resource
def initialize_face_recognition() -> tuple[FaceDataManager, FaceRecognizer]:
    """Initialize face recognition components."""
    logger.info("Initializing face recognition components...")
    
    data_manager = FaceDataManager(logger=logger)
    faces_count = data_manager.build_database_from_images()
    
    if faces_count == 0:
        logger.warning("WARNING: Database is empty!")
    else:
        logger.info("Database loaded: %d faces", faces_count)
    
    recognizer = FaceRecognizer(data_manager=data_manager, logger=logger)
    return data_manager, recognizer


def render_sidebar(data_manager: FaceDataManager) -> None:
    """Render sidebar with statistics and settings."""
    st.sidebar.title("⚙️ Settings")
    st.sidebar.subheader("📊 Database")
    db_info = data_manager.get_database_info()
    
    st.sidebar.metric(label="Total faces", value=db_info["total_faces"])
    st.sidebar.metric(label="Unique persons", value=db_info["unique_persons"])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Actions")
    
    if st.sidebar.button("🔄 Rebuild Database", use_container_width=True):
        with st.spinner("Rebuilding database..."):
            data_manager.clear_database()
            faces_count = data_manager.build_database_from_images(force_rebuild=True)
            
            if faces_count > 0:
                st.sidebar.success(f"✅ {faces_count} faces trained!")
                logger.info("Database rebuilt: %d faces", faces_count)
                st.rerun()
            else:
                st.sidebar.error("❌ No faces found!")
    
    if st.sidebar.button("🗑️ Clear Cache", use_container_width=True):
        cache_file = config.ENCODINGS_FILE
        if cache_file.exists():
            cache_file.unlink()
            st.sidebar.success("✅ Cache cleared!")
            logger.info("Cache file deleted")
        else:
            st.sidebar.info("ℹ️ No cache file found")
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Tip**: Place images in `data/people/` folder, "
        "one subfolder per person!"
    )


def save_new_image_and_retrain(
    data_manager: FaceDataManager,
    image: Image.Image,
    recognized_faces: list[tuple[str, tuple[int, int, int, int]]],
    original_filename: str
) -> bool:
    """
    Save image to person folders and add encodings to database.
    
    Args:
        data_manager: FaceDataManager instance
        image: PIL Image to save
        recognized_faces: List of (name, location) tuples
        original_filename: Original filename for reference
        
    Returns:
        True if successful, False otherwise
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        success_count = 0
        
        for idx, (person_name, _) in enumerate(recognized_faces):
            # Skip unknown faces
            if person_name == "Ismeretlen":
                continue
            
            # Create person folder if it doesn't exist
            person_folder = config.PEOPLE_DIR / person_name.replace(" ", "_")
            person_folder.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            filename = f"confirmed_{timestamp}_{idx}.jpg"
            save_path = person_folder / filename
            
            # Save image
            image.save(save_path, "JPEG")
            logger.info("Saved image to %s", save_path)
            
            # Add encoding to database
            if data_manager.add_single_image_encoding(save_path, person_name):
                success_count += 1
                logger.info("Added encoding for %s", person_name)
            else:
                logger.warning("Failed to add encoding for %s", person_name)
        
        return success_count > 0
        
    except Exception as e:
        logger.error("Error saving image and retraining: %s", str(e))
        return False


def render_main_content(recognizer: FaceRecognizer, data_manager: FaceDataManager) -> None:
    """Render main content (image upload, recognition)."""
    st.title(config.APP_TITLE)
    st.markdown("---")
    
    with st.expander("ℹ️ How it works?", expanded=False):
        st.markdown("""
        ### Usage
        1. **Upload an image** using the uploader below
        2. Click **"Ki van a képen?"** button
        3. The app will **detect all faces** in the image
        4. **Compare** with local database
        5. **Confirm** if the recognition is correct
        
        ### Privacy
        - ✅ 100% local, no cloud
        - ✅ Images stored in `data/people/` folder
        - ✅ GDPR compliant (with consent)
        
        ### Supported formats
        - JPG, JPEG, PNG, BMP, GIF
        """)
    
    st.markdown("---")
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader(
        label="Choose an image",
        type=["jpg", "jpeg", "png", "bmp", "gif"],
        help=f"Maximum size: {config.MAX_UPLOAD_SIZE_MB} MB"
    )
    
    if uploaded_file is not None:
        # Load and fix image orientation
        image = Image.open(uploaded_file)
        image = fix_image_orientation(image)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🖼️ Uploaded Image")
            
            # Show annotated image if we have recognized faces
            if (st.session_state.current_image is not None and 
                st.session_state.recognized_faces and 
                st.session_state.current_filename == uploaded_file.name):
                
                annotated_image = draw_face_annotations(
                    st.session_state.current_image,
                    st.session_state.recognized_faces
                )
                st.image(annotated_image, use_column_width=True)
            else:
                st.image(image, use_column_width=True)
            
            st.caption(
                f"File: {uploaded_file.name} | "
                f"Size: {image.size[0]}x{image.size[1]} px"
            )
        
        with col2:
            st.subheader("🔍 Result")
            
            # Recognition button
            if st.button("🚀 Ki van a képen?", type="primary", use_container_width=True):
                with st.spinner("Arcok felismerése..."):
                    recognized_faces = recognizer.recognize_all_faces(image)
                    
                    if not recognized_faces:
                        st.warning("### ❓ Nem találtam arcot a képen")
                        st.info("Próbálj jobb minőségű képet feltölteni.")
                        logger.info("No faces found (file: %s)", uploaded_file.name)
                        
                        # Clear session state
                        st.session_state.recognized_faces = []
                        st.session_state.current_image = None
                        st.session_state.awaiting_confirmation = False
                    else:
                        # Store in session state
                        st.session_state.recognized_faces = recognized_faces
                        st.session_state.current_image = image
                        st.session_state.current_filename = uploaded_file.name
                        st.session_state.awaiting_confirmation = True
                        
                        # Count known vs unknown
                        known_faces = [name for name, _ in recognized_faces if name != "Ismeretlen"]
                        unknown_count = len([name for name, _ in recognized_faces if name == "Ismeretlen"])
                        
                        if known_faces:
                            st.success(f"### ✅ Felismertem: **{', '.join(known_faces)}**")
                            logger.info("Recognized: %s (file: %s)", ', '.join(known_faces), uploaded_file.name)
                            
                            if unknown_count > 0:
                                st.warning(f"⚠️ Emellett {unknown_count} ismeretlen arcot is találtam")
                        else:
                            st.warning(f"### ❓ {len(recognized_faces)} ismeretlen arc")
                            st.info("Ezek az arcok nincsenek az adatbázisban.")
                        
                        st.rerun()
            
            # Confirmation dialog
            if st.session_state.awaiting_confirmation and st.session_state.recognized_faces:
                known_faces = [name for name, _ in st.session_state.recognized_faces if name != "Ismeretlen"]
                
                if known_faces:
                    st.markdown("---")
                    if len(known_faces) == 1:
                        st.info(f"💬 Valóban **{known_faces[0]}** van a képen?")
                    else:
                        st.info(f"💬 Valóban **{', '.join(known_faces)}** vannak a képen?")
                    
                    col_yes, col_no = st.columns(2)
                    
                    with col_yes:
                        if st.button("✅ Igen", use_container_width=True, type="primary"):
                            if st.session_state.current_image is None or st.session_state.current_filename is None:
                                st.error("❌ Hiba: nincs betöltött kép")
                            else:
                                with st.spinner("Képek mentése és tanulás..."):
                                    if save_new_image_and_retrain(
                                        data_manager,
                                        st.session_state.current_image,
                                        st.session_state.recognized_faces,
                                        st.session_state.current_filename
                                    ):
                                        st.success("✅ Kép elmentve és adatbázis frissítve!")
                                        st.balloons()
                                        logger.info("Image saved and database updated")
                                        
                                        # Clear session state
                                        st.session_state.awaiting_confirmation = False
                                        st.session_state.recognized_faces = []
                                        st.session_state.current_image = None
                                        st.session_state.current_filename = None
                                        
                                        st.rerun()
                                    else:
                                        st.error("❌ Hiba történt a mentés során")
                    
                    with col_no:
                        if st.button("❌ Nem", use_container_width=True):
                            st.error("### 🤬 Szopdki ocskos, tudom hogy jól számoltam!")
                            st.balloons()
                            logger.info("User rejected recognition")
                            
                            # Clear session state
                            st.session_state.awaiting_confirmation = False
                            st.session_state.recognized_faces = []
                            st.session_state.current_image = None
                            st.session_state.current_filename = None
            
            # Detailed analysis expander
            if st.session_state.recognized_faces:
                with st.expander("📊 Részletes Elemzés", expanded=False):
                    st.markdown("**Talált arcok:**")
                    for idx, (name, location) in enumerate(st.session_state.recognized_faces, start=1):
                        top, right, bottom, left = location
                        st.markdown(f"{idx}. **{name}** (pozíció: {left}, {top} - {right}, {bottom})")



def render_empty_database_warning(data_manager: FaceDataManager) -> None:
    """Show warning if database is empty."""
    db_info = data_manager.get_database_info()
    
    if db_info["total_faces"] == 0:
        st.error("### ⚠️ Database is empty!")
        st.markdown("""
        **Steps to populate the database:**
        
        1. Open the project folder: `data/people/`
        2. Create subfolders for each person (e.g., `John_Doe`)
        3. Place images in the subfolders (more images = better recognition)
        4. Click **"🔄 Rebuild Database"** button in the sidebar
        
        **Example structure:**
        ```
        data/people/
        ├── John_Doe/
        │   ├── photo1.jpg
        │   └── photo2.jpg
        └── Jane_Smith/
            └── photo1.jpg
        ```
        """)
        
        st.info(f"📁 Full path: `{config.PEOPLE_DIR.absolute()}`")


def main() -> None:
    """Application entry point."""
    try:
        initialize_session_state()
        data_manager, recognizer = initialize_face_recognition()
        render_sidebar(data_manager)
        render_empty_database_warning(data_manager)
        render_main_content(recognizer, data_manager)
        
    except Exception as e:
        st.error("### ❌ Critical error occurred!")
        st.exception(e)
        logger.critical("Critical error in main(): %s", str(e), exc_info=True)


if __name__ == "__main__":
    main()
