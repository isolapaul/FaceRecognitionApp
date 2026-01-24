"""Authentication module for user management."""
import hashlib
import logging
import re
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import bcrypt as bcrypt_module

try:
    import bcrypt as bcrypt_module
    BCRYPT_AVAILABLE = True
except ImportError:
    bcrypt_module = None  # type: ignore
    BCRYPT_AVAILABLE = False

from src.database import DatabaseManager


logger = logging.getLogger(__name__)


class AuthManager:
    """Handle user authentication and registration."""
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager
        self.use_bcrypt = BCRYPT_AVAILABLE
        
        if not self.use_bcrypt:
            logger.warning("bcrypt not available! Using fallback hashing (NOT SECURE!)")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt or fallback."""
        if self.use_bcrypt and bcrypt_module is not None:
            salt = bcrypt_module.gensalt()
            hashed = bcrypt_module.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        else:
            # FALLBACK - NOT FOR PRODUCTION!
            return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        if self.use_bcrypt and bcrypt_module is not None:
            return bcrypt_module.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        else:
            # FALLBACK - NOT FOR PRODUCTION!
            return hashlib.sha256(password.encode('utf-8')).hexdigest() == password_hash
    
    def validate_username(self, username: str) -> tuple[bool, str]:
        """
        Validate username format.
        
        Returns:
            (is_valid, error_message)
        """
        if not username:
            return False, "Felhasználónév nem lehet üres"
        
        if len(username) < 3:
            return False, "Felhasználónév legalább 3 karakter legyen"
        
        if len(username) > 50:
            return False, "Felhasználónév maximum 50 karakter lehet"
        
        # Only alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Csak betűk, számok és alulvonás használható"
        
        return True, ""
    
    def validate_password(self, password: str) -> tuple[bool, str]:
        """
        Validate password strength.
        
        Returns:
            (is_valid, error_message)
        """
        if not password:
            return False, "Jelszó nem lehet üres"
        
        if len(password) < 6:
            return False, "Jelszó legalább 6 karakter legyen"
        
        if len(password) > 128:
            return False, "Jelszó maximum 128 karakter lehet"
        
        return True, ""
    
    def register(self, username: str, password: str) -> tuple[bool, str]:
        """
        Register a new user.
        
        Returns:
            (success, message)
        """
        # Validate username
        valid, error = self.validate_username(username)
        if not valid:
            return False, error
        
        # Validate password
        valid, error = self.validate_password(password)
        if not valid:
            return False, error
        
        # Check if username exists
        if self.db.user_exists(username):
            return False, "Ez a felhasználónév már foglalt"
        
        # Hash password and create user
        password_hash = self._hash_password(password)
        user_id = self.db.create_user(username, password_hash)
        
        if user_id:
            logger.info("User registered: %s (id: %d)", username, user_id)
            return True, f"Sikeres regisztráció! Üdv, {username}!"
        else:
            return False, "Regisztráció sikertelen. Próbáld újra!"
    
    def login(self, username: str, password: str) -> tuple[bool, Optional[dict], str]:
        """
        Authenticate user.
        
        Returns:
            (success, user_data, message)
        """
        if not username or not password:
            return False, None, "Felhasználónév és jelszó kötelező"
        
        user = self.db.get_user(username)
        
        if not user:
            return False, None, "Hibás felhasználónév vagy jelszó"
        
        if self._verify_password(password, user['password_hash']):
            logger.info("User logged in: %s", username)
            return True, user, f"Üdv újra, {username}!"
        else:
            return False, None, "Hibás felhasználónév vagy jelszó"
