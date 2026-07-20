# -*- coding: utf-8 -*-
"""Scheduler for Central Bank Engine"""


class CentralBankScheduler:
    def schedule(self):
        """Define central bank engine schedule"""
        return {
            "interval": "*/1 * * * *",  # Every minute
            "priority": 1,
            "retries": 3,
            "timeout": 60,
        }

    def run(self):
        """Execute central bank data collection"""
        pass
