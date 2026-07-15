"""Universal Hub Standard.

Every workspace in Nexus AI Terminal MUST implement a Hub following this standard.
The Hub is the central coordination point for all intelligence within a workspace.

Required Components:
- Repository: Data storage and retrieval
- Providers: Data source management
- Dispatcher: Event routing
- History: Historical tracking
- Health: Health monitoring
- Search: Search capabilities
- API: API endpoints
- AI: AI integration
"""

__all__ = [
    "HubConfig",
    "HubStatus",
    "HubHealth",
]
