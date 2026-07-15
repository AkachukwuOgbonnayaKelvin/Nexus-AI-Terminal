"""Authentication service.

Provides authentication and authorization.
"""

from .auth import AuthManager, User

__all__ = ["AuthManager", "User"]
