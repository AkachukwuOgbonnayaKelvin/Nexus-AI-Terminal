import os

os.environ["NEXUS_DB_TYPE"] = "postgresql"
os.environ["NEXUS_DATABASE_URL"] = (
    "postgresql://postgres:6468@localhost/nexus_ai_terminal"
)

from datetime import datetime

from intelligence.data.common.writer import DataWriter

writer = DataWriter()
tick = {
    "symbol": "EURUSD",
    "timestamp": datetime.utcnow().isoformat(),
    "bid": 1.12345,
    "ask": 1.12355,
    "last": 1.12350,
    "volume": 100.0,
    "source_id": "test_write",
    "quality_score": 0.9,
}
inserted = writer.write_ticks([tick])
print(f"Inserted: {inserted}")
