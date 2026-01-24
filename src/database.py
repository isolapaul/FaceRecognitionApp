"""Database connection and management."""
import os
import logging
import sqlite3
from typing import Optional, TYPE_CHECKING, Any
from contextlib import contextmanager

if TYPE_CHECKING:
    import psycopg2
    from psycopg2.extras import RealDictCursor

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    psycopg2 = None  # type: ignore
    RealDictCursor = None  # type: ignore
    POSTGRES_AVAILABLE = False


logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manage database connections (PostgreSQL or SQLite fallback)."""
    
    def __init__(self) -> None:
        self.db_url = os.getenv("DATABASE_URL")
        self.use_postgres = POSTGRES_AVAILABLE and self.db_url is not None
        
        if self.use_postgres:
            logger.info("Using PostgreSQL database")
        else:
            logger.info("Using SQLite database (local mode)")
            # SQLite fallback for local development
            self.sqlite_path = "data/app_database.db"
    
    @contextmanager
    def get_connection(self) -> Any:
        """Get database connection (context manager)."""
        if self.use_postgres and psycopg2 is not None:
            conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
        else:
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = sqlite3.Row
        
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error("Database error: %s", str(e))
            raise
        finally:
            conn.close()
    
    def initialize_database(self) -> None:
        """Create tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            if self.use_postgres:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
            logger.info("Database initialized successfully")
    
    def create_user(self, username: str, password_hash: str) -> Optional[int]:
        """Create a new user."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.use_postgres:
                    cursor.execute(
                        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
                        (username, password_hash)
                    )
                    result = cursor.fetchone()
                    return result['id'] if result else None
                else:
                    cursor.execute(
                        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        (username, password_hash)
                    )
                    return cursor.lastrowid
                    
        except Exception as e:
            logger.error("Error creating user: %s", str(e))
            return None
    
    def get_user(self, username: str) -> Optional[dict]:
        """Get user by username."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.use_postgres:
                    cursor.execute(
                        "SELECT id, username, password_hash, created_at FROM users WHERE username = %s",
                        (username,)
                    )
                else:
                    cursor.execute(
                        "SELECT id, username, password_hash, created_at FROM users WHERE username = ?",
                        (username,)
                    )
                
                result = cursor.fetchone()
                return dict(result) if result else None
                
        except Exception as e:
            logger.error("Error getting user: %s", str(e))
            return None
    
    def user_exists(self, username: str) -> bool:
        """Check if username already exists."""
        user = self.get_user(username)
        return user is not None
