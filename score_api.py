import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATABASE = os.environ.get("SCORES_DB", "scores.db")


def init_db():
    """Create the scores table if it doesn't exist."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        # Index for faster top-score queries
        conn.execute("CREATE INDEX IF NOT EXISTS idx_score ON scores(score DESC)")


if __name__ == "__main__":
    init_db()
