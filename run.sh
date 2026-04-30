#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check for --rebuild flag
PORT=5000

REBUILD=""
if [ "$1" = "--rebuild" ]; then
    REBUILD="--build"
    echo -e "${YELLOW}Rebuilding image...${NC}"
fi

echo -e "${GREEN}🐍 Starting Snake Game...${NC}"

# 1. Free port 5000 on the host (if something else is using it)
echo "Checking for processes using port $PORT..."

# Find the PID(s) using the port (works on Linux/macOS)
# Using lsof to get PIDs listening on TCP port 5000
PIDS=$(lsof -ti :$PORT 2>/dev/null)

if [ -n "$PIDS" ]; then
    echo "Killing process(es): $PIDS"
    kill -9 $PIDS
    echo "Processes killed."
else
    echo "No process found using port $PORT."
fi

# Optional: Wait a moment for port to be released
sleep 1

# 2. Deduplicate scores (keep earliest per player/score/second) – only if table exists
echo "Cleaning duplicate scores..."
if [ -f scores.db ]; then
    python3 -c "
import sqlite3
conn = sqlite3.connect('scores.db')
conn.execute('''
    DELETE FROM scores
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM scores
        GROUP BY player_name, score, substr(timestamp, 1, 19)
    )
''')
conn.commit()
deleted = conn.total_changes
conn.close()
print(f'Removed {deleted} duplicate rows.')
"
else
    echo "No scores.db yet – skipping deduplication."
fi

# GROUP BY player_name, score, substr(timestamp, 1, 19)
# Groups rows that have the same:
# * player_name (e.g., "Alice")
# * score (e.g., 123)
# * The date and time up to the second (ignoring microseconds) – because substr(timestamp, 1, 19) extracts the first 19 characters of the ISO timestamp (e.g., 2026-04-29T19:17:29 from 2026-04-29T19:17:29.401352).
# All entries from the same second are considered duplicates.
# * SELECT MIN(id)
#   For each group (same player, same score, same second), it picks the smallest id. In SQLite, id is an AUTOINCREMENT primary key, so the smallest id is the earliest inserted record in that group.
#   Result of subquery: a list of ids that should be kept (one per duplicate group).


# 3.Allow Docker to access X11 display
xhost +local:docker

# 4. Set display environment variable
export DISPLAY=$DISPLAY

# 5. Start both services (snake-game + score-api)
docker compose up $REBUILD

# 6. Cleanup after game closes (Ctrl+C or exit)
echo -e "${YELLOW}Cleaning up...${NC}"
xhost -local:docker
docker compose down

echo -e "${GREEN}Game closed!${NC}"

