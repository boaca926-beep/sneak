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
| **P** / **Any Key** | Pause the game / Resume the game|
| **R** | Restart game (after game over) |
| **Q** | Quit game |

### Game Rules
1. Control the snake to eat the red food blocks
2. Each food eaten increases score by 1
3. The snake grows longer after eating
4. Game ends if the snake:
   - Hits the wall
   - Collides with its own body
5. You win if the snake fills the entire grid!

## 🚀 Quick Start
```bash
# For Ubuntu system
./run.sh --rebuild
```

```text
--rebuild forces a fresh Docker image rebuild (useful after dependency changes).
```

- ✅ Detect if Docker is installed

- ✅ Start Docker daemon if needed

- ✅ Automatically fix permission issues (new!)

- ✅ Clean up port 5000

- ✅ Start the Snake Game

- ✅ Clean up when done

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

<p align="center">
  <img src="figures/game_end.png" alt="Top-10 scores output" width="400">
  <img src="figures/snake_output.png" alt="Top-10 scores output" width="400">
</p>

3. **Rebuild Docker image if needed**
```bash
./run.sh --rebuild
```

## X11 Security Note
The script uses xhost +local:docker for simplicity. On multi‑user systems, use a more restrictive command:
```bash
xhost +SI:localuser:root
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
├── score_api.py          # Flask API + SQLite leaderboard
├── leaderboard.html      # Auto‑refreshing web leaderboard
├── my_game.py            # Legacy/alternative game entry point
├── docker-compose.yml    # Docker orchestration
├── Dockerfile            # Docker image definition
├── run.sh                # Quick start script (with Docker & API)
├── inspect_db.sh         # SQLite inspection helper
├── requirements.txt      # Python dependencies (pip)
├── pyproject.toml        # Project metadata (PEP 621)
├── uv.lock               # uv package manager lock file
├── scores.db             # SQLite database (created at runtime)
├── figures/              # Screenshots for README (game_end.png, etc.)
└── scripts/              # Additional helper scripts (if any)
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
DISPLAY=${DISPLAY}              # X11 display for GUI
ENABLE_DEBUG=${ENABLE_DEBUG}    # Debug mode toggle
QT_X11_NO_MITSHM=1              # X11 shared memory fix
LIBGL_ALWAYS_SOFTWARE=1         # Software rendering fallback
```

## 🎯 Future Enhancements
Potential features to add:

- ✅ Pause function (press P, and to resume press any key)
- ✅ Multiple difficulty levels (speed increases over time)
- ✅ High score tracking with persistent storage
- Power-ups and special food types
- Sound effects and background music
- Two-player mode
- AI-controlled snake for demo mode
```python
# from re import S
# from time import sleep

from cmd import PROMPT
from operator import le
from urllib import response
import webbrowser
import os
from collections import deque          # for BFS

from flask import request
import pygame
import random
import sys
import requests

# Initialize Pygame
pygame.init()

# ========================== GAME MODES ==========================
VS_AI = True           # Set to True for Human vs AI, False for single‑player
# ================================================================

# Constants; game basic attributions
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 0)
BLUE = (0, 100, 200)          # AI snake colour
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
DARK_BLUE = (0, 50, 100)
GRAY = (50, 50, 50)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# API endpoint
API_BASE = "http://localhost:5000"

# Level progression (for human)
LEVEL_EVERY = 5


def random_food_position(snake, snake2=None):
    """
    Generate a random position not occupied by any snake.
    """
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        pos = (x, y)
        if pos not in snake and (snake2 is None or pos not in snake2):
            return pos


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_snake(screen, snake, color, border_color):
    """Draw a snake with any colour."""
    for segment in snake:
        rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, border_color, rect, 2)


def draw_food(screen, food):
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, (200, 0, 0), rect, 2)


def show_score(screen, font, score, player_name="", level=1, x=10, y=10):
    """Display score for a player (default top‑left)."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    name_text = font.render(f"{player_name}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (x, y))
    screen.blit(name_text, (x, y + 30))
    screen.blit(level_text, (x, y + 60))


def show_game_over(screen, font, score, player_name="", winner=None):
    """Display game over message, optionally a winner."""
    screen.fill(BLACK)
    if winner:
        game_over_text = font.render(f"{winner} WINS!", True, RED)
    else:
        game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    name_text = font.render(f"Player: {player_name}", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2,
                                 HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2,
                             HEIGHT // 2 - 20))
    screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2,
                            HEIGHT // 2 + 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2,
                               HEIGHT // 2 + 60))
    pygame.display.flip()


def show_paused(screen, font):
    paused_text = font.render("PAUSED", True, WHITE)
    resume_text = font.render("Press any key to resume", True, WHITE)
    screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2,
                              HEIGHT // 2 - 30))
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2,
                              HEIGHT // 2 + 20))
    pygame.display.flip()


def get_player_name(screen, font):
    """Get player name before game starts."""
    name = ""
    input_active = True
    cursor_visible = True
    cursor_timer = 0

    prompt_text = font.render("Enter player's name: ", True, WHITE)
    instruction_text = font.render("Press Enter to start, ESC to default",
                                   True, GRAY)

    while input_active:
        screen.fill(BLACK)

        title_text = font.render("SNAKE GAME", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2,
                                 HEIGHT // 2 - 150))

        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2,
                                  HEIGHT // 2 - 50))

        display_name = name
        if cursor_visible:
            display_name += "_"
        name_surface = font.render(display_name, True, GREEN)
        screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2,
                                   HEIGHT // 2))

        screen.blit(instruction_text,
                    (WIDTH // 2 - instruction_text.get_width() // 2,
                     HEIGHT // 2 + 80))

        pygame.display.flip()

        cursor_timer += 1
        if cursor_timer >= 300:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name:
                        input_active = False
                    else:
                        name = "Player"
                        input_active = False
                elif event.key == pygame.K_ESCAPE:
                    name = "Player"
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if (len(name) < 15 and event.unicode.isprintable()
                            and event.unicode != ""):
                        name += event.unicode

    return name if name else "Player"


def reset_game():
    """Reset human snake (single‑player or player 1) to start position."""
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = RIGHT
    next_direction = RIGHT
    score = 0
    return snake, direction, next_direction, score


def reset_ai_snake():
    """Reset AI snake to a mirrored starting position."""
    start_x = GRID_WIDTH - GRID_WIDTH // 2 - 1
    start_y = GRID_HEIGHT // 2
    snake = [(start_x, start_y), (start_x + 1, start_y), (start_x + 2, start_y)]
    direction = LEFT
    next_direction = LEFT
    score = 0
    return snake, direction, next_direction, score


def ai_next_direction(snake, food, other_snake=None):
    """
    BFS shortest path from snake head to food.
    Avoids walls, own body, and the other snake's body.
    Returns a safe direction (UP/DOWN/LEFT/RIGHT).
    """
    head = snake[0]
    grid_w, grid_h = GRID_WIDTH, GRID_HEIGHT

    # blocked cells: own body (except tail will move, but we include it for safety)
    blocked = set(snake[1:])
    if other_snake is not None:
        blocked.update(other_snake)      # avoid hitting the other snake

    queue = deque([(head, [])])
    visited = {head}

    dirs = [(UP, (0, -1)), (DOWN, (0, 1)), (LEFT, (-1, 0)), (RIGHT, (1, 0))]

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == food:
            return path[0] if path else None

        for direction, (dx, dy) in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_w and 0 <= ny < grid_h:
                if (nx, ny) not in blocked and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [direction]))

    # No path found → pick a safe move that does not cause immediate death
    for direction, (dx, dy) in dirs:
        nx, ny = head[0] + dx, head[1] + dy
        if 0 <= nx < grid_w and 0 <= ny < grid_h:
            if (nx, ny) not in snake[1:]:
                if other_snake is None or (nx, ny) not in other_snake:
                    return direction
    return UP   # fallback


def send_score_to_api(player_name, score, level):
    url = f"{API_BASE}/score"
    payload = {"player_name": player_name, "score": int(score), "level": level}
    try:
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 201:
            print(f"Score saved: {player_name} - {score} (level {level})")
        else:
            print(f"Failed to save score: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending score to API: {e}")


# The main program
def main():
    global FPS

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Get player name (human)
    player_name = get_player_name(screen, font)

    # Difficulty selection (hardcoded to easy for now)
    print("\nChoose difficulty level: 1=Easy (slow), 2=Medium, 3=Hard (fast)")
    diff = "1"
    base_fps = {"1": 6, "2": 10, "3": 14}.get(diff, 10)
    FPS = base_fps
    MAX_FPS = base_fps + 5
    starting_fps = FPS
    SPEED_INCREMENT = 0.5
    INCREMENT_EVERY = 3

    # Open leaderboard in browser if possible
    leaderboard_url = "http://localhost:5000/leaderboard"
    try:
        if os.environ.get("DISPLAY"):
            webbrowser.open(leaderboard_url)
    except Exception:
        pass

    # ----- Game state (single or two‑player) -----
    game_over = False
    game_over_sent = False
    paused = False

    # Human player (always present)
    snake, direction, next_direction, score = reset_game()
    level = 1

    # AI opponent (only if VS_AI is True)
    if VS_AI:
        snake_ai, direction_ai, next_direction_ai, score_ai = reset_ai_snake()
        level_ai = 1
    else:
        snake_ai = None
        direction_ai = None
        next_direction_ai = None
        score_ai = 0
        level_ai = 0

    # Initial food (no collision)
    food = random_food_position(snake, snake_ai)

    winner = None          # stores who won (if any)
    running = True

    while running:
        # ----- Event Handling -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if not paused:
                        # Human controls only when not game over and not paused
                        if event.key == pygame.K_UP and direction != DOWN:
                            next_direction = UP
                        elif event.key == pygame.K_DOWN and direction != UP:
                            next_direction = DOWN
                        elif event.key == pygame.K_LEFT and direction != RIGHT:
                            next_direction = LEFT
                        elif event.key == pygame.K_RIGHT and direction != LEFT:
                            next_direction = RIGHT
                        elif event.key == pygame.K_p:
                            paused = True
                    else:
                        if event.key == pygame.K_q:
                            running = False
                            pygame.quit()
                            sys.exit()
                        else:
                            paused = False
                else:
                    # Game over – restart or quit
                    if event.key == pygame.K_r:
                        # Reset everything
                        snake, direction, next_direction, score = reset_game()
                        level = 1
                        if VS_AI:
                            (snake_ai, direction_ai,
                             next_direction_ai, score_ai) = reset_ai_snake()
                            level_ai = 1
                        food = random_food_position(snake, snake_ai)
                        game_over = False
                        game_over_sent = False
                        paused = False
                        FPS = starting_fps
                        winner = None
                    elif event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        sys.exit()

        # ----- Pause handling -----
        if paused and not game_over:
            screen.fill(BLACK)
            draw_grid(screen)
            draw_food(screen, food)
            draw_snake(screen, snake, GREEN, DARK_GREEN)
            if VS_AI:
                draw_snake(screen, snake_ai, BLUE, DARK_BLUE)
            show_score(screen, font, score, player_name, level, 10, 10)
            if VS_AI:
                show_score(screen, font, score_ai, "AI", level_ai,
                           WIDTH - 150, 10)
            show_paused(screen, font)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # ----- Game logic (only if not game over) -----
        if not game_over:
            # ---- Human snake movement ----
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # ---- AI snake movement (if VS_AI) ----
            if VS_AI:
                ai_dir = ai_next_direction(snake_ai, food, other_snake=snake)
                if ai_dir:
                    # Prevent reversing
                    if ((ai_dir == UP and direction_ai != DOWN) or
                        (ai_dir == DOWN and direction_ai != UP) or
                        (ai_dir == LEFT and direction_ai != RIGHT) or
                        (ai_dir == RIGHT and direction_ai != LEFT)):
                        direction_ai = ai_dir
                head_ai_x, head_ai_y = snake_ai[0]
                dx_ai, dy_ai = direction_ai
                new_head_ai = (head_ai_x + dx_ai, head_ai_y + dy_ai)

            # ---- Food collision checks ----
            ate_food_human = (new_head == food)
            ate_food_ai = (VS_AI and new_head_ai == food)

            # Human eats food
            if ate_food_human:
                snake.insert(0, new_head)
                score += 1.5
                new_level = int(score) // LEVEL_EVERY + 1
                if new_level > level:
                    level = new_level
                    FPS = min(MAX_FPS, FPS + SPEED_INCREMENT)
                # New food, avoid both snakes
                free_cells = [(x, y) for x in range(GRID_WIDTH)
                              for y in range(GRID_HEIGHT)
                              if (x, y) not in snake
                              and (not VS_AI or (x, y) not in snake_ai)]
                if not free_cells:
                    game_over = True
                    winner = player_name   # human filled the grid
                    continue
                food = random.choice(free_cells)
            else:
                snake.insert(0, new_head)
                snake.pop()

            # AI eats food
            if VS_AI and ate_food_ai:
                snake_ai.insert(0, new_head_ai)
                score_ai += 1.5
                new_level_ai = int(score_ai) // LEVEL_EVERY + 1
                if new_level_ai > level_ai:
                    level_ai = new_level_ai
                    # Optionally increase FPS for AI too – same speed for fairness
                    # FPS = min(MAX_FPS, FPS + SPEED_INCREMENT)
                # Regenerate food (avoid both snakes)
                free_cells = [(x, y) for x in range(GRID_WIDTH)
                              for y in range(GRID_HEIGHT)
                              if (x, y) not in snake and (x, y) not in snake_ai]
                if not free_cells:
                    game_over = True
                    winner = "AI"
                    continue
                food = random.choice(free_cells)
            elif VS_AI:
                snake_ai.insert(0, new_head_ai)
                snake_ai.pop()

            # ---- Collision detection ----
            # Human snake collisions (walls, self, AI)
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake[1:] or
                (VS_AI and new_head in snake_ai)):
                game_over = True
                winner = "AI" if VS_AI else None

            # AI snake collisions (if not already game over)
            if VS_AI and not game_over:
                if (new_head_ai[0] < 0 or new_head_ai[0] >= GRID_WIDTH or
                    new_head_ai[1] < 0 or new_head_ai[1] >= GRID_HEIGHT or
                    new_head_ai in snake_ai[1:] or
                    new_head_ai in snake):
                    game_over = True
                    winner = player_name   # human wins

        # ----- Drawing -----
        screen.fill(BLACK)
        draw_grid(screen)
        draw_food(screen, food)
        draw_snake(screen, snake, GREEN, DARK_GREEN)
        if VS_AI:
            draw_snake(screen, snake_ai, BLUE, DARK_BLUE)

        # Display scores (human left, AI right if two‑player)
        show_score(screen, font, score, player_name, level, 10, 10)
        if VS_AI:
            show_score(screen, font, score_ai, "AI", level_ai, WIDTH - 150, 10)

        if game_over:
            if not game_over_sent:
                # Only save human score to leaderboard
                send_score_to_api(player_name, score, level)
                game_over_sent = True
            # Show game over with winner
            show_game_over(screen, font, score, player_name, winner)
        elif paused:
            show_paused(screen, font)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    print("Starting Snake Game (Human vs AI mode)...")
    main()
```
- Different maze/wall configurations

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Error response from daemon: Conflict" | docker system prune -a && docker volume prune |
| "Cannot connect to X server" | `xhost +local:docker` and `export DISPLAY=$DISPLAY` |
| Pygame won't install | `sudo apt-get install python3-pygame` (Ubuntu) |
| Game runs too fast/slow | Adjust `FPS` in `snake.py` (higher = faster, lower = slower) |
| Docker GUI not showing | `export LIBGL_ALWAYS_SOFTWARE=1` |
| Leaderboard shows no data | Ensure API is running on `localhost:5000` before opening `leaderboard.html` |
| Port 5000 already in use | `fuser -k 5000/tcp` (Linux) or stop the process using the port |

## Flask API with SQLite that stores the highest scores and allows retrieval of the top 10.
```bash
score_api.py
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

## Persistent Storage in Docker
Add a volume to docker-compose.yml to keep scores.db across container restarts:
```yaml
volumes:
  - ./data:/app/data
```

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

### 1. Create leaderboard.html in the project folder
```bash
leaderboard.html
```
<p align="center">
  <img src="figures/top10_web.png" alt="Top-10 scores output" width="600">
</p>

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

- The docker-compose.yml already maps "5000:5000", so the host can reach it.

- The browser (running on local host) will fetch http://localhost:5000/top-scores without any problem.
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

## How to evolve this project toward data engineering

-Replace SQLite with PostgreSQL (or use both). Add Docker Compose service for Postgres. Show you can connect to a production‑grade database.

- Add a data pipeline: every time a score is submitted, also write to a raw log table. Create a scheduled job (e.g., inside the API) that aggregates daily top scores into a summary table (leaderboard snapshot).

- Implement a simple ETL script: export scores to a CSV/Parquet file, or load them into a second database for analytics.

- Use environment‑aware config – expand to load different configs for dev/prod.

- Add metrics / monitoring: track number of scores per hour, average score, etc. Expose via a new /stats endpoint.

- Containerize with Airflow (complex but impressive): create a DAG that runs deduplication SQL every hour instead of at game start.

- Push to cloud storage: after the game is closed, automatically upload scores.db to S3 or Google Cloud Storage.
## Add a Desktop short-cut with icon
**Create $HOME/.local/share/applications/snake-game.desktop with:**
```bash
Version=1.0
Name=Snake Game
Comment=Play the Snake Game in a Docker container
Exec=gnome-terminal --working-directory=$HOME/Desktop/sneak -- bash -c "./run.sh; echo 'Press Enter to exit...'; read"
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Game;
StartupNotify=true
```

**Update the script**
```bash
update-desktop-database ~/.local/share/applications/
# Change ownership
chmod +x ~/.local/share/applications/snake-game.desktop
```

**Add a Desktop short-cut with icon**
```bash
cp ~/.local/share/applications/snake-game.desktop ~/Desktop/
# Test run
gtk-launch snake-game.desktop
```
Replace gnome-terminal with xterm if needed. Place a custom snake-icon.png in ~/.local/share/icons/.

**Update the desktop database:**
```bash
update-desktop-database ~/.local/share/applications/
chmod +x ~/.local/share/applications/snake-game.desktop
```

**Add a Desktop shortcut:**
```bash
cp ~/.local/share/applications/snake-game.desktop ~/Desktop/
# Test run
gtk-launch snake-game.desktop
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

## Note
A Deeper Clean and Clean Up Unused Volumes
```bash
alias docker-clean='docker system prune -a && docker volume prune'
```
