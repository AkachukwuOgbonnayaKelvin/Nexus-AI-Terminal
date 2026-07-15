"""Database service.

Provides database connection pooling, session management, and migrations.
"""

from .connection import close_session, get_session

__all__ = ["get_session", "close_session"]
