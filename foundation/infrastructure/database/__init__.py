"""Database service.

Provides database connection pooling, session management, and migrations.
"""

from .connection import close_session, get_session

__all__ = ["close_session", "get_session"]
