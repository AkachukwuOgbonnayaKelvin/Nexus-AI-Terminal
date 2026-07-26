"""WebSocket manager."""


class WebSocketManager:
    """WebSocket connection manager."""

    def __init__(self) -> None:
        self._connections: set[str] = set()

    def connect(self, client_id: str) -> None:
        """Register a WebSocket connection."""
        self._connections.add(client_id)

    def disconnect(self, client_id: str) -> None:
        """Unregister a WebSocket connection."""
        self._connections.discard(client_id)

    def broadcast(self, message: str) -> None:
        """Broadcast a message to all clients."""
        # In production, this would send via WebSocket

    def get_connections(self) -> int:
        """Get the number of active connections."""
        return len(self._connections)
