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
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Bo","score":350}'

# Get top 10 scores
curl http://localhost:5000/top-scores
```

## Run as a Background Service
