from datetime import datetime, timedelta

from intelligence.data.tick.coverage.planner import SyncPlanner

planner = SyncPlanner()
now = datetime.utcnow()
target_start = now - timedelta(days=3)
plan = planner.plan("EURUSD", target_start, now)

print("=== SYNC PLAN ===\n")
print(f"Symbol: {plan.symbol}")
print(f"Target: {plan.target_start} -> {plan.target_end}")
print(f"Status: {plan.status}")
print(f"Historical gaps: {len(plan.historical_gaps)}")
print(f"Recent gaps: {len(plan.recent_gaps)}")
print(f"Total jobs: {len(plan.jobs)}\n")
for job in plan.jobs:
    print(f"  Job {job.job_id}: {job.job_type.value} | {job.start} -> {job.end}")
