# -*- coding: utf-8 -*-
"""Scheduler for Financial News Engine"""


class NewsScheduler:
    def schedule(self):
        """Define news engine schedule"""
        return {
            "interval": "*/1 * * * *",  # Every minute
            "priority": 2,
            "retries": 3,
            "timeout": 30,
        }

    def run(self):
        """Execute news collection"""
        pass
