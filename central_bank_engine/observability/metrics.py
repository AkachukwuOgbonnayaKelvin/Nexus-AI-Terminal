from collections import defaultdict


class MetricsCollector:
    def __init__(self):
        self.counters = defaultdict(int)
        self.timers = defaultdict(list)

    def increment(self, name: str):
        self.counters[name] += 1

    def record_time(self, name: str, duration: float):
        self.timers[name].append(duration)
        if len(self.timers[name]) > 1000:
            self.timers[name].pop(0)

    def get_counter(self, name: str) -> int:
        return self.counters.get(name, 0)

    def get_avg_time(self, name: str) -> float:
        timings = self.timers.get(name, [])
        if timings:
            return sum(timings) / len(timings)
        return 0.0

    def get_metrics(self) -> dict:
        return {
            "counters": dict(self.counters),
            "avg_timings": {k: self.get_avg_time(k) for k in self.timers.keys()},
        }


metrics = MetricsCollector()
