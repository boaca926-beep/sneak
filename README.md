# Snake Game 🐍

A classic Snake game built with Python and Pygame. Control a snake, eat food to grow longer, and try to achieve the highest score!

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.6.1+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎮 Game Features

- Classic snake mechanics - eat food to grow longer
- Smooth keyboard controls (arrow keys)
- Score tracking with player name input
- Self-collision and wall collision detection
- Game over screen with restart option
- Grid visualization for better gameplay

## 🎯 How to Play

### Controls
| Key | Action |
|-----|--------|
| ⬆️ Up Arrow | Move snake up |
| ⬇️ Down Arrow | Move snake down |
| ⬅️ Left Arrow | Move snake left |
| ➡️ Right Arrow | Move snake right |
| **R** | Restart game (after game over) |
| **Q** | Quit game |

### Game Rules
1. Control the snake to eat the red food blocks
2. Each food eaten increases your score by 1
3. The snake grows longer after eating
4. Game ends if the snake:
   - Hits the wall
   - Collides with its own body
5. You win if the snake fills the entire grid!

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/boaca926-beep/sneak.git
cd snake-game
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
# or
pip install pygame
```

3. **Run the game**
```bash
python snake.py
# or if using the original file
python my_game.py
```

## 🐳 Docker Setup (For Linux with X11)

1. **Make the run script executable**
```bash
chmod +x run.sh
```

2. **Start the game**
```bash
./run.sh
```

3. **Rebuild Docker image if needed**
```bash
./run.sh --rebuild
```

## Docker Configuration
The project includes Docker support for consistent development environments, especially useful for Linux systems with GUI forwarding.

### docker-compose.yml Features
- X11 display forwarding for GUI rendering

- Volume mounting for live code updates

- Network host mode for display access

- Environment variables for debugging and X11 configuration

### Manual Docker Commands
```bash
# Build the image
docker build -t snake-game .

# Run with GUI support
xhost +local:docker
docker compose up
docker compose down
xhost -local:docker
```

## 📁 Project Structure
```text
snake-game/
├── snake.py              # Main game implementation
├── docker-compose.yml   # Docker orchestration
├── run.sh              # Quick start script
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project metadata
└── README.md           # This file
```

## Customization Options
Edit snake.py to modify game behavior:

| Variable | Description | Default |
|----------|-------------|---------|
| `CELL_SIZE` | Size of each grid cell (pixels) | 30 |
| `GRID_WIDTH` | Number of grid columns | 20 |
| `GRID_HEIGHT` | Number of grid rows | 20 |
| `FPS` | Game speed (frames per second) | 5 |
| Colors | RGB values for visual elements | Various |

## Color Customization
```python
BLACK = (0, 0, 0)        # Background
GREEN = (0, 200, 0)      # Snake body
DARK_GREEN = (0, 150, 0) # Snake border
RED = (255, 0, 0)        # Food
GRAY = (50, 50, 50)      # Grid lines
WHITE = (200, 200, 200)  # Text
```

## 🛠️ Development

### Prerequisites

- Python 3.12 or higher

- Pygame 2.6.1+

- Docker (optional, for containerized execution)

- X11 server (for Linux GUI support)

### Environment Variables (Docker)
```bash
DISPLAY=${DISPLAY}           # X11 display for GUI
ENABLE_DEBUG=${ENABLE_DEBUG} # Debug mode toggle
QT_X11_NO_MITSHM=1          # X11 shared memory fix
LIBGL_ALWAYS_SOFTWARE=1      # Software rendering fallback
```

## 🎯 Future Enhancements
Potential features to add:

- High score tracking with persistent storage

- Multiple difficulty levels (speed increases over time)

- Power-ups and special food types

- Sound effects and background music

- Two-player mode

- AI-controlled snake for demo mode

- Different maze/wall configurations

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Cannot connect to X server"
```bash
# Solution: Allow Docker to access X11
xhost +local:docker
export DISPLAY=$DISPLAY
```

#### Issue: Pygame won't install
```bash
# Solution: Install system dependencies
# Ubuntu/Debian
sudo apt-get install python3-pygame

# macOS
brew install pygame
```

#### Issue: Game runs too fast/slow
```python
# Solution: Adjust FPS in snake.py
FPS = 10  # Higher = faster, Lower = slower
```

#### Issue: Docker GUI not showing
```bash
# Solution: Use software rendering
export LIBGL_ALWAYS_SOFTWARE=1
```

## Flask API with SQLite that stores the highest scores and allows retrieval of the top 10.
```python
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = "scores.db"

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
        # Index for faster top‑score queries
        conn.execute("CREATE INDEX IF NOT EXISTS idx_score ON scores(score DESC)")

@app.route("/score", methods=["POST"])
def add_score():
    """
    Expects JSON: {"player_name": "Alice", "score": 123}
    Stores the score in the database.
    """
    data = request.get_json()
    if not data or "player_name" not in data or "score" not in data:
        return jsonify({"error": "Missing player_name or score"}), 400

    player_name = data["player_name"][:50]          # limit length
    score = data["score"]
    timestamp = datetime.utcnow().isoformat()

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO scores (player_name, score, timestamp) VALUES (?, ?, ?)",
            (player_name, score, timestamp)
        )
    return jsonify({"message": "Score saved"}), 201

@app.route("/top-scores", methods=["GET"])
def get_top_scores():
    """Return the top 10 highest scores."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "SELECT player_name, score, timestamp FROM scores ORDER BY score DESC LIMIT 10"
        )
        rows = cursor.fetchall()
    top_scores = [
        {"player_name": row[0], "score": row[1], "timestamp": row[2]} for row in rows
    ]
    return jsonify(top_scores)

@app.route("/scores", methods=["GET"])
def get_all_scores():
    """(Optional) Return all scores, newest first."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "SELECT player_name, score, timestamp FROM scores ORDER BY timestamp DESC"
        )
        rows = cursor.fetchall()
    all_scores = [
        {"player_name": row[0], "score": row[1], "timestamp": row[2]} for row in rows
    ]
    return jsonify(all_scores)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
```
### Run the API
```bash
python score_api.py

# Add a score
#curl -X POST http://localhost:5000/score \
#  -H "Content-Type: application/json" \
#  -d '{"player_name":"Bo","score":350}'

# Get top 10 scores
curl http://localhost:5000/top-scores
```

## Run as a Background Service

## Inspect Database
```bash
# Run SQlite
./inspect_db.sh
```

**Operations**
```sql
.tables          -- should show 'scores'
.schema scores   -- see table structure
SELECT * FROM scores;
```

## Auto‑refreshing leaderboard window

### 1. Create leaderboard.html in your project folder
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Snake Game – Top Scores</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #1e1e2f;
            color: #ffffff;
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #00cc66;
        }
        table {
            margin: 0 auto;
            border-collapse: collapse;
            width: 80%;
            max-width: 600px;
            background: #2d2d3a;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #444;
        }
        th {
            background: #0f0f1a;
            color: #00cc66;
            font-size: 1.2em;
        }
        tr:hover {
            background: #3a3a4a;
        }
        .refresh-note {
            margin-top: 20px;
            font-size: 0.8em;
            color: #aaa;
        }
    </style>
</head>
<body>
    <h1>🐍 TOP SCORES</h1>
    <div id="leaderboard">
        <p>Loading scores...</p>
    </div>
    <div class="refresh-note">Updates every 10 seconds</div>

    <script>
        function fetchScores() {
            fetch('http://localhost:5000/top-scores')
                .then(response => response.json())
                .then(data => {
                    let html = '<table><tr><th>Rank</th><th>Player</th><th>Score</th><th>Date</th></tr>';
                    data.forEach((entry, index) => {
                        const date = new Date(entry.timestamp).toLocaleString();
                        html += `<tr>
                                    <td>${index+1}</td>
                                    <td>${escapeHtml(entry.player_name)}</td>
                                    <td>${entry.score}</td>
                                    <td>${date}</td>
                                 </tr>`;
                    });
                    html += '</table>';
                    document.getElementById('leaderboard').innerHTML = html;
                })
                .catch(err => {
                    document.getElementById('leaderboard').innerHTML = '<p style="color:red">Error loading scores. Make sure the API is running on port 5000.</p>';
                    console.error(err);
                });
        }

        function escapeHtml(str) {
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }

        // Fetch immediately, then every 10 seconds
        fetchScores();
        setInterval(fetchScores, 10000);
    </script>
</body>
</html>
```

### 2. Modify snake.py to open the leaderboard
```python
import webbrowser   # add at the top

# ... inside main(), after getting player_name:

# Open the leaderboard window (only once)
leaderboard_path = os.path.join(os.path.dirname(__file__), "leaderboard.html")
webbrowser.open(f"file://{leaderboard_path}", new=2)  # new=2 opens in new tab if possible
```

### 3. Make sure the API is reachable
```bash
- The score-api container must be running and accessible on localhost:5000.

- Your docker-compose.yml already maps "5000:5000", so the host can reach it.

- The browser (running on your host) will fetch http://localhost:5000/top-scores without any problem.
```

### 4. Full integration to snake.py
```python
# At the top
import webbrowser
import os

# Inside main(), after player_name is known:
leaderboard_url = f"file://{os.path.abspath('leaderboard.html')}"
webbrowser.open(leaderboard_url)
```

```bash
How to evolve this project toward data engineering

    Replace SQLite with PostgreSQL (or use both).

        Add Docker Compose service for Postgres.

        Show you can connect to a production‑grade database.

    Add a data pipeline

        Every time a score is submitted, also write to a raw log table.

        Create a scheduled job (e.g., inside the API) that aggregates daily top scores into a summary table (leaderboard snapshot).

    Implement a simple ETL script

        Export scores to a CSV/Parquet file.

        Or load them into a second database for analytics.

    Use environment‑aware config

        Already partially done – expand to load different configs for dev/prod.

    Add metrics / monitoring

        Track number of scores per hour, average score, etc. Expose via a new /stats endpoint.

    Containerize with Airflow (complex but impressive)

        Create a DAG that runs the deduplication SQL every hour instead of at game start.

    Push to a cloud storage

        After the game is closed, automatically upload scores.db to S3 or Google Cloud Storage.
```
## Add a Desktop short-cut with icon
```bash
# Add bash script /home/bo/.local/share/applications/snake-game.desktop
# Change ownership: chmod +x snake-game.deskop
Version=1.0
Name=Snake Game
Comment=Play the Snake Game in a Docker container
Exec=gnome-terminal --working-directory=/home/bo/Desktop/sneak -- bash -c "./run.sh; echo 'Press Enter to exit...'; read"
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Game;
StartupNotify=true
```

**Add snake-game.desktop**
```bash
Name=Snake Game
Comment=Play the Snake Game in a Docker container
Exec=gnome-terminal -- bash -c "cd /home/bo/Desktop/sneak && export LIBGL_ALWAYS_SOFTWARE=1 && export SDL_VIDEODRIVER=x11 && ./run.sh; echo 'Game closed. Press Enter to exit...'; read"
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Game;
StartupNotify=true
Icon=/home/bo/.local/share/icons/snake-icon.png
```

## For Data Engineer
```bash
- ETL pipeline that ingests a public dataset (e.g., weather or stock data) into PostgreSQL, cleans it, and exposes via API.

- Use Airflow (Dockerised) to schedule the pipeline.

- Write data to Parquet and AWS S3 (free tier).
```

## For ML/AI Engineer
```bash
For ML / AI Engineer

- Deploy a pre‑trained model (e.g., Hugging Face sentiment analysis) as a REST API with Docker.

- Add the RL Snake as described earlier – train an agent to play.

- Create a model retraining pipeline (trigger retraining when new scores arrive).
```
