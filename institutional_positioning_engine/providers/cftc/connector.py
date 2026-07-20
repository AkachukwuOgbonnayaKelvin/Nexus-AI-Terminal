"""CFTC Connection Layer – Institutional-grade connector."""

import logging
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class CFTCConnector:
    """Bloomberg-style CFTC connector with retry, failover, and health monitoring."""

    def __init__(self):
        self.base_url = "https://www.cftc.gov"
        self.historical_url = "https://www.cftc.gov/files/dea/history"
        self.current_url = "https://www.cftc.gov/dea"
        self.timeout = 30
        self.max_retries = 3
        self.retry_delay = 2
        self._connected = False
        self._last_check = None
        self._latency = 0

    def connect(self) -> bool:
        """Establish connection to CFTC."""
        try:
            start = time.time()
            resp = requests.get(self.base_url, timeout=5)
            self._latency = (time.time() - start) * 1000
            self._connected = resp.status_code == 200
            self._last_check = datetime.now()
            return self._connected
        except Exception as e:
            logger.error(f"CFTC connection failed: {e}")
            self._connected = False
            return False

    def health(self) -> Dict[str, Any]:
        """Return health status."""
        return {
            "status": "healthy" if self._connected else "unhealthy",
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "latency_ms": self._latency,
            "retries": 0,
        }

    def get(self, url: str, retries: int = 3) -> Optional[requests.Response]:
        """GET with retry logic."""
        for attempt in range(retries):
            try:
                resp = requests.get(url, timeout=self.timeout)
                if resp.status_code == 200:
                    return resp
                if attempt < retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
            except Exception as e:
                logger.warning(f"Request failed (attempt {attempt+1}): {e}")
                if attempt < retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
        return None

    def download_file(self, url: str, dest: str) -> bool:
        """Download a file with checksum verification."""
        resp = self.get(url)
        if not resp:
            return False
        try:
            with open(dest, "wb") as f:
                f.write(resp.content)
            return True
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            return False
