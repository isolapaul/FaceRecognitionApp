"""Face Recognition Streamlit Application."""
import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st
from PIL import Image

import config
from src.utils import setup_logging, fix_image_orientation, draw_face_annotations
from src.database import DatabaseManager
from src.auth import AuthManager

# Lazy imports to avoid loading face_recognition before it's needed
if TYPE_CHECKING:
    from src.data_manager import FaceDataManager
    from src.face_engine import FaceRecognizer


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
    # Authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
    
    # Face recognition
    if "awaiting_confirmation" not in st.session_state:
        st.session_state.awaiting_confirmation = False
    if "recognized_faces" not in st.session_state:
        st.session_state.recognized_faces = []
    if "current_image" not in st.session_state:
        st.session_state.current_image = None
    if "current_filename" not in st.session_state:
        st.session_state.current_filename = None


@st.cache_resource
def initialize_face_recognition(user_id: int) -> tuple:
    """Initialize face recognition components for specific user."""
    # Import here to avoid loading face_recognition before login
    from src.data_manager import FaceDataManager
    from src.face_engine import FaceRecognizer
    
    logger.info("Initializing face recognition components for user_id: %d...", user_id)
    
    data_manager = FaceDataManager(user_id=user_id, logger=logger)
    faces_count = data_manager.build_database_from_images()
    
    if faces_count == 0:
        logger.warning("WARNING: Database is empty for user_id: %d!", user_id)
    else:
        logger.info("Database loaded: %d faces for user_id: %d", faces_count, user_id)
    
    recognizer = FaceRecognizer(data_manager=data_manager, logger=logger)
    return data_manager, recognizer


@st.cache_resource
def get_db_manager() -> DatabaseManager:
    """Get database manager instance."""
    db = DatabaseManager()
    db.initialize_database()
    return db


@st.cache_resource
def get_auth_manager() -> AuthManager:
    """Get authentication manager instance."""
    return AuthManager(get_db_manager())


def render_login_page(auth_manager: AuthManager) -> None:
    """Render login/register page."""
    st.title("🎭 Face Recognition App")
    st.markdown("---")
    
    # Toggle between login and register
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.show_register:
            st.subheader("📝 Regisztráció")
            
            with st.form("register_form"):
                username = st.text_input("Felhasználónév", max_chars=50)
                password = st.text_input("Jelszó", type="password", max_chars=128)
                password_confirm = st.text_input("Jelszó megerősítés", type="password", max_chars=128)
                
                col_reg, col_back = st.columns(2)
                
                with col_reg:
                    submit = st.form_submit_button("Regisztráció", type="primary", use_container_width=True)
                
                with col_back:
                    back = st.form_submit_button("Vissza a belépéshez", use_container_width=True)
                
                if submit:
                    if not username or not password:
                        st.error("❌ Töltsd ki az összes mezőt!")
                    elif password != password_confirm:
                        st.error("❌ A jelszavak nem egyeznek!")
                    else:
                        success, message = auth_manager.register(username, password)
                        if success:
                            st.success(f"✅ {message}")
                            st.info("Most már beléphetsz az új fiókodba!")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                
                if back:
                    st.session_state.show_register = False
                    st.rerun()
        
        else:
            st.subheader("🔐 Bejelentkezés")
            
            with st.form("login_form"):
                username = st.text_input("Felhasználónév")
                password = st.text_input("Jelszó", type="password")
                
                col_login, col_register = st.columns(2)
                
                with col_login:
                    submit = st.form_submit_button("Belépés", type="primary", use_container_width=True)
                
                with col_register:
                    register_btn = st.form_submit_button("Regisztráció", use_container_width=True)
                
                if submit:
                    if not username or not password:
                        st.error("❌ Töltsd ki az összes mezőt!")
                    else:
                        success, user, message = auth_manager.login(username, password)
                        if success and user:
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                
                if register_btn:
                    st.session_state.show_register = True
                    st.rerun()
    
    # Info box
    st.markdown("---")
    with st.expander("ℹ️ Információ", expanded=False):
        st.markdown("""
        ### Üdvözlünk! 👋
        
        Ez egy **arcfelismerő alkalmazás**, ahol:
        - ✅ Feltölthetsz képeket ismerősökről
        - ✅ Az app megtanulja felismerni őket
        - ✅ Később automatikusan megnevezi ki van a képen
        - ✅ Minden felhasználó saját adatbázist használ
        
        **Kezdéshez:**
        1. Regisztrálj egy új fiókot
        2. Lépj be
        3. Töltsd fel az első képeket!
        """)


def render_sidebar(data_manager) -> None:
    """Render sidebar with statistics and settings."""
    # User info and logout
    if st.session_state.user:
        st.sidebar.title(f"👤 {st.session_state.user['username']}")
        
        if st.sidebar.button("🚪 Kijelentkezés", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.awaiting_confirmation = False
            st.session_state.recognized_faces = []
            st.session_state.current_image = None
            st.session_state.current_filename = None
            st.cache_resource.clear()  # Clear cached resources
            st.rerun()
        
        st.sidebar.markdown("---")
    
    st.sidebar.title("⚙️ Beállítások")
    st.sidebar.subheader("📊 Adatbázis")
    db_info = data_manager.get_database_info()
    
    st.sidebar.metric(label="Összes arc", value=db_info["total_faces"])
    st.sidebar.metric(label="Egyedi személyek", value=db_info["unique_persons"])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Műveletek")
    
    if st.sidebar.button("🔄 Adatbázis újraépítése", use_container_width=True):
        with st.spinner("Adatbázis újraépítése..."):
            data_manager.clear_database()
            faces_count = data_manager.build_database_from_images(force_rebuild=True)
            
            if faces_count > 0:
                st.sidebar.success(f"✅ {faces_count} arc betanítva!")
                logger.info("Database rebuilt: %d faces", faces_count)
                st.rerun()
            else:
                st.sidebar.info("ℹ️ Még nincsenek képek az adatbázisban")
    
    if st.sidebar.button("🗑️ Cache törlése", use_container_width=True):
        cache_file = data_manager.encodings_file
        if cache_file.exists():
            cache_file.unlink()
            st.sidebar.success("✅ Cache törölve!")
            logger.info("Cache file deleted")
        else:
            st.sidebar.info("ℹ️ Nincs cache fájl")
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        f"💡 **Tipp**: Képeket a `{data_manager.people_dir}` mappába tedd, "
        "minden személynek külön almappa!"
    )


def save_new_image_and_retrain(
    data_manager,
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
            
            # Create person folder if it doesn't exist (use data_manager's people_dir)
            person_folder = data_manager.people_dir / person_name.replace(" ", "_")
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


def render_main_content(recognizer, data_manager) -> None:
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



def render_empty_database_warning(data_manager) -> None:
    """Show warning if database is empty."""
    db_info = data_manager.get_database_info()
    
    if db_info["total_faces"] == 0:
        st.info("### ℹ️ Az adatbázis még üres")
        st.markdown(f"""
        **Lépések az adatbázis feltöltéséhez:**
        
        1. Nyisd meg a projekt mappát: `{data_manager.people_dir}`
        2. Hozz létre almappákat minden személyhez (pl. `Kovacs_Janos`)
        3. Tedd a képeket az almappákba (több kép = jobb felismerés)
        4. Kattints az **"🔄 Adatbázis újraépítése"** gombra az oldalsávban
        
        **Példa struktúra:**
        ```
        {data_manager.people_dir.name}/
        ├── Kovacs_Janos/
        │   ├── photo1.jpg
        │   └── photo2.jpg
        └── Nagy_Anna/
            └── photo1.jpg
        ```
        """)
        
        st.info(f"📁 Teljes útvonal: `{data_manager.people_dir.absolute()}`")


def main() -> None:
    """Application entry point."""
    try:
        initialize_session_state()
        
        # Check if user is authenticated
        if not st.session_state.authenticated or not st.session_state.user:
            auth_manager = get_auth_manager()
            render_login_page(auth_manager)
            return
        
        # User is authenticated - show main app
        user_id = st.session_state.user['id']
        
        # Show loading message while initializing face recognition
        with st.spinner('🔄 Arcfelismerő rendszer betöltése... (Ez az első alkalommal 30-60 másodpercet vehet igénybe)'):
            data_manager, recognizer = initialize_face_recognition(user_id)
        
        render_sidebar(data_manager)
        render_empty_database_warning(data_manager)
        render_main_content(recognizer, data_manager)
        
    except Exception as e:
        st.error("### ❌ Kritikus hiba történt!")
        st.exception(e)
        logger.critical("Critical error in main(): %s", str(e), exc_info=True)


if __name__ == "__main__":
    main()
