"""
Data Health Checker – validates database connectivity and reports status.
"""

import time
from enum import Enum
from dataclasses import dataclass
from sqlalchemy import create_engine, text


class DataSourceStatus(Enum):
    HEALTHY = "healthy"
    UNAVAILABLE = "unavailable"
    AUTH_FAILED = "auth_failed"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


@dataclass
class DataHealthReport:
    status: DataSourceStatus
    message: str
    latency_ms: float


class DataHealthChecker:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def check(self) -> DataHealthReport:
        try:
            engine = create_engine(self.db_url, connect_args={"connect_timeout": 3})
            with engine.connect() as conn:
                start = time.time()
                result = conn.execute(text("SELECT 1"))
                end = time.time()
                if result.scalar() == 1:
                    return DataHealthReport(
                        status=DataSourceStatus.HEALTHY,
                        message="Database connection successful",
                        latency_ms=(end - start) * 1000,
                    )
        except Exception as e:
            error_msg = str(e)
            if "password authentication failed" in error_msg:
                status = DataSourceStatus.AUTH_FAILED
                message = "PostgreSQL authentication failed. Check credentials."
            elif "timeout" in error_msg:
                status = DataSourceStatus.TIMEOUT
                message = "Database connection timed out."
            else:
                status = DataSourceStatus.UNAVAILABLE
                message = f"Database unavailable: {error_msg}"
            return DataHealthReport(status=status, message=message, latency_ms=0.0)
