"""Face Recognition Streamlit Application."""
import logging

import streamlit as st
from PIL import Image

import config
from src.data_manager import FaceDataManager
from src.face_engine import FaceRecognizer
from src.utils import setup_logging


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


def render_main_content(recognizer: FaceRecognizer) -> None:
    """Render main content (image upload, recognition)."""
    st.title(config.APP_TITLE)
    st.markdown("---")
    
    with st.expander("ℹ️ How it works?", expanded=False):
        st.markdown("""
        ### Usage
        1. **Upload an image** using the uploader below
        2. The app will **automatically detect the face**
        3. **Compare** with local database
        4. **Show the result** (name or "Unknown")
        
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
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🖼️ Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            st.caption(
                f"File: {uploaded_file.name} | "
                f"Size: {image.size[0]}x{image.size[1]} px"
            )
        
        with col2:
            st.subheader("🔍 Result")
            
            if st.button("🚀 Recognize Face", type="primary", use_container_width=True):
                with st.spinner("Recognizing face..."):
                    recognized_name = recognizer.recognize_face(image)
                    
                    if recognized_name:
                        st.success(f"### ✅ Recognized: **{recognized_name}**")
                        logger.info("Successful recognition: %s (file: %s)", recognized_name, uploaded_file.name)
                    else:
                        st.warning("### ❓ Unknown Face")
                        st.info("Face not found in database or no face detected in image.")
                        logger.info("Unknown face (file: %s)", uploaded_file.name)
                    
                    with st.expander("📊 Detailed Analysis", expanded=False):
                        detailed_results = recognizer.get_detailed_match_results(image, top_n=5)
                        
                        if detailed_results:
                            st.markdown("**Top 5 matches:**")
                            
                            for idx, (name, distance) in enumerate(detailed_results, start=1):
                                confidence = max(0, 100 - (distance * 100))
                                st.metric(
                                    label=f"{idx}. {name}",
                                    value=f"{confidence:.1f}%",
                                    delta=f"Distance: {distance:.3f}"
                                )
                        else:
                            st.warning("Could not analyze image")


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
        data_manager, recognizer = initialize_face_recognition()
        render_sidebar(data_manager)
        render_empty_database_warning(data_manager)
        render_main_content(recognizer)
        
    except Exception as e:
        st.error("### ❌ Critical error occurred!")
        st.exception(e)
        logger.critical("Critical error in main(): %s", str(e), exc_info=True)


if __name__ == "__main__":
    main()
