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


@app.route("/score", methods=["POST"])
def add_score():
    """
    Expects JSON: {"player_name": "Alice", "score": 123}
    Stores the score in the database.
    """
    data = request.get_json()
    if not data or "player_name" not in data or "score" not in data:
        # If either condition is true, it returns an error response with HTTP 400
        return jsonify({"error": "Missing player_name or score"}), 400

    player_name = data["player_name"][:50]  # Limit name length

    try:
        score = int(data["score"])
    except (ValueError, TypeError):
        return jsonify({"error": "score must be an integer"}), 400

    if score < 0:
        return jsonify({"error": "score must be non-negative"}), 400

    timestamp = datetime.utcnow().isoformat()

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO scores (player_name, score, timestamp) VALUES (?, ?, ?)",
            (player_name, score, timestamp),
        )
    return jsonify({"message": "Score saved successfully"}), 201


@app.route("/top-scores", methods=["GET"])
def get_top_scores():
    """
    Returns the top 10 scores in JSON format.
    """
    with sqlite3.connect(DATABASE) as conn:
        # DESC: Sorts the scores in descending order, so the highest scores come first.
        cursor = conn.execute(
            "SELECT player_name, score, timestamp FROM scores ORDER BY score DESC LIMIT 10"
        )
        rows = cursor.fetchall()
    top_scores = [{"player_name": row[0], "score": row[1], "timestamp": row[2]} for row in rows]
    return jsonify(top_scores)


@app.route("/scores", methods=["GET"])
def get_all_scores():
    """
    Returns all scores in JSON format, sorted by timestamp decending.
    """
    limit = request.args.get(
        "limit", default=100, type=int
    )  #  the fallback value when no limit parameter is given. So if the URL is just /scores (no ?limit=...), limit will be set to 100.
    limit = max(1, min(limit, 1000))  # At least 1, at most 1000
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "SELECT player_name, score, timestamp FROM scores ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
    all_scores = [{"player_name": row[0], "score": row[1], "timestamp": row[2]} for row in rows]
    return jsonify(all_scores)


@app.route("/leaderboard")
def leaderboard():
    from flask import send_file

    return send_file("leaderboard.html")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
