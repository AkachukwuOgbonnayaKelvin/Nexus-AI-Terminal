#!/bin/bash
# Stop the OHLC sync service

if [ -f logs/ohlc_sync.pid ]; then
    PID=$(cat logs/ohlc_sync.pid)
    if ps -p "$PID" > /dev/null 2>&1; then
        kill -TERM "$PID"
        sleep 2
        if ps -p "$PID" > /dev/null 2>&1; then
            kill -9 "$PID"
        fi
        rm -f logs/ohlc_sync.pid
        echo "OHLC sync service stopped (PID: $PID)"
    else
        echo "OHLC sync service not running (stale PID file)"
        rm -f logs/ohlc_sync.pid
    fi
else
    echo "OHLC sync service not running (no PID file)"
fi
