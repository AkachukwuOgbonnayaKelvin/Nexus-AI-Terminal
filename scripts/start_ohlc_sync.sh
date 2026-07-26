#!/bin/bash
# Start the OHLC sync service in the background

cd "$(dirname "$0")/.." || exit

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if already running
if [ -f logs/ohlc_sync.pid ]; then
    PID=$(cat logs/ohlc_sync.pid 2>/dev/null)
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "OHLC sync service is already running (PID: $PID)"
        exit 1
    fi
fi

# Start the service (use 'python' or 'python3' - adjust if needed)
nohup python3 scripts/ohlc_sync_service.py >> logs/ohlc_sync.out 2>&1 &
PID=$!
echo $PID > logs/ohlc_sync.pid
echo "OHLC sync service started (PID: $PID)"
echo "Logs: tail -f logs/ohlc_sync.log"
