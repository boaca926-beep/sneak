#!/bin/bash
docker run --rm -v "$(pwd):/data" -it keinos/sqlite3 sqlite3 /data/scores.db
