# -*- coding: utf-8 -*-
"""Scheduler for DAR runtime"""


class EngineScheduler:
    def schedule(self):
        return {"interval": "*/5 * * * *", "priority": 3}

    def run(self):
        pass
