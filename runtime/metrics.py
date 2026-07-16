import time
from collections import defaultdict


class MetricsCollector:
    def __init__(self):
        self.run_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.last_run_times = {}
        self.durations = defaultdict(list)

    def record_run(self, engine_name: str, success: bool, duration: float):
        self.run_counts[engine_name] += 1
        self.last_run_times[engine_name] = time.time()
        self.durations[engine_name].append(duration)
        if len(self.durations[engine_name]) > 100:
            self.durations[engine_name].pop(0)
        if not success:
            self.error_counts[engine_name] += 1

    def get_metrics(self, engine_name: str):
        durations = self.durations.get(engine_name, [])
        avg_duration = sum(durations) / len(durations) if durations else 0
        return {
            "runs": self.run_counts.get(engine_name, 0),
            "errors": self.error_counts.get(engine_name, 0),
            "last_run": self.last_run_times.get(engine_name),
            "avg_duration_ms": avg_duration * 1000,
        }

    def get_all_metrics(self, engines):
        return {e.name: self.get_metrics(e.name) for e in engines}


metrics = MetricsCollector()
