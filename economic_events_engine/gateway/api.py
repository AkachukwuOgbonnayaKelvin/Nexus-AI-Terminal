# -*- coding: utf-8 -*-
"""API gateway for external consumers"""

class EngineGateway:
    def __init__(self):
        self.routes = {}
    def register_route(self, path, handler):
        self.routes[path] = handler
    def handle_request(self, path, data):
        if path in self.routes:
            return self.routes[path](data)
        return {"error": "Route not found"}
