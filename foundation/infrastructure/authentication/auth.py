"""Authentication service."""

from typing import Dict, Optional


class User:
    """User representation."""

    def __init__(self, username: str, roles: list = None):
        self.username = username
        self.roles = roles or []


class AuthManager:
    """Authentication manager."""

    def __init__(self):
        self._users: Dict[str, User] = {}
        self._tokens: Dict[str, str] = {}

    def register_user(self, username: str, password: str) -> None:
        """Register a new user."""
        # In production, this would hash the password
        self._users[username] = User(username)

    def login(self, username: str, password: str) -> Optional[str]:
        """Login a user."""
        if username in self._users:
            # In production, this would validate password
            token = f"token_{username}"
            self._tokens[token] = username
            return token
        return None

    def logout(self, token: str) -> None:
        """Logout a user."""
        self._tokens.pop(token, None)

    def validate_token(self, token: str) -> Optional[User]:
        """Validate an authentication token."""
        username = self._tokens.get(token)
        if username:
            return self._users.get(username)
        return None
