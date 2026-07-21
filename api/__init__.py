"""
API Layer

Exposes the workspace snapshot to clients.
"""

from .routes import router

__all__ = [
    "router",
]
