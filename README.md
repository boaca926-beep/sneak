```python
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 10  # Game speed (moves per second)

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
GRAY = (50, 50, 50)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def random_food_position(snake):
    """Generate a random position that is not occupied by the snake."""
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)

def draw_grid(screen):
    """Draw grid lines for better visibility."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_snake(screen, snake):
    """Draw the snake on the screen."""
    for segment in snake:
        rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)
        pygame.draw.rect(screen, DARK_GREEN, rect, 2)  # border

def draw_food(screen, food):
    """Draw the food (a red square)."""
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, (200, 0, 0), rect, 2)

def show_score(screen, font, score):
    """Display the current score."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over(screen, font, score):
    """Display game over message and final score."""
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)

    # Center the messages
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
    pygame.display.flip()

def reset_game():
    """Reset game variables for a new round."""
    # Initial snake: three cells in the middle, moving right
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x, start_y), (start_x-1, start_y), (start_x-2, start_y)]
    direction = RIGHT
    next_direction = RIGHT
    food = random_food_position(snake)
    score = 0
    return snake, direction, next_direction, food, score

def main():
    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Game state
    game_over = False
    snake, direction, next_direction, food, score = reset_game()

    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    # Change direction based on key press (prevent 180-degree turns)
                    if event.key == pygame.K_UP and direction != DOWN:
                        next_direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        next_direction = DOWN
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        next_direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        next_direction = RIGHT
                else:
                    # When game over, check for restart or quit
                    if event.key == pygame.K_r:
                        # Reset everything
                        snake, direction, next_direction, food, score = reset_game()
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        sys.exit()

        if not game_over:
            # --- Update Game Logic ---
            direction = next_direction  # Apply the queued direction

            # Calculate new head position
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Check for food collision
            ate_food = (new_head == food)

            # Perform movement
            if ate_food:
                # Insert new head without removing tail (snake grows)
                snake.insert(0, new_head)
                score += 10
                # Generate new food at a position not occupied by the snake
                free_cells = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) if (x, y) not in snake]
                if not free_cells:
                    # Snake has filled the grid - player wins
                    game_over = True
                    continue
                food = random.choice(free_cells)
            else:
                # Normal move: insert new head and remove tail
                snake.insert(0, new_head)
                snake.pop()

            # --- Collision Detection ---
            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                game_over = True
                continue

            # Check self collision (head colliding with body)
            if new_head in snake[1:]:
                game_over = True
                continue

        # --- Drawing ---
        screen.fill(BLACK)          # Clear screen
        draw_grid(screen)           # Optional grid
        draw_food(screen, food)     # Draw food
        draw_snake(screen, snake)   # Draw snake
        show_score(screen, font, score)  # Show score

        if game_over:
            show_game_over(screen, font, score)

        pygame.display.flip()       # Update display
        clock.tick(FPS)             # Control game speed

if __name__ == "__main__":
    main()
```

## File Structure
```bash
snake-game/
├── main.py                    # Your game code
├── requirements.txt           # Dependencies
├── Dockerfile                 # Single dev-focused stage
├── .dockerignore
├── docker-compose.yml        # Just dev config
├── .env.example
└── scripts/
    └── entrypoint.sh          # Dev setup script
```
## 1. Requirements File
```text
pygame
```

## Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Pygame
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    libfreetype6 \
    xvfb \           # Virtual display (for headless fallback)
    vim \            # Useful for debugging
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install dev tools (optional but handy)
RUN pip install ipython debugpy

# Copy game code
COPY snake.py .

# Copy entrypoint
COPY scripts/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "-u", "main.py"]

EXPOSE 5678  # Debug port
```

## 3. Entrypoint Script
**scripts/entrypoint.sh**
```bash
#!/bin/bash
set -e

echo "🐍 Snake Game - DEV MODE"
echo "========================"
echo "X11 Display: ${DISPLAY}"
echo "Debug port: 5678"

# Check if X11 socket is available (for GUI)
if [ -n "$DISPLAY" ] && [ -e "/tmp/.X11-unix/X${DISPLAY#*:}" ]; then
    echo "✅ X11 forwarding detected - GUI will be displayed"
else
    echo "⚠️  No X11 forwarding - running with virtual display"
    Xvfb :99 -screen 0 1024x768x24 &
    export DISPLAY=:99
fi

# Start debugpy server for remote debugging (optional)
if [ "${ENABLE_DEBUG:-false}" = "true" ]; then
    echo "🐛 Debugger listening on port 5678"
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py &
    DEBUG_PID=$!
    wait $DEBUG_PID
else
    # Execute the command
    exec "$@"
fi
```

## 4. Docker Compose Files
**docker-compose.yml (Dev - auto-loaded)**
```yaml
version: '3.8'

services:
  snake-game:
    build: .
    environment:
      - DISPLAY=${DISPLAY}
      - ENABLE_DEBUG=${ENABLE_DEBUG:-false}
    volumes:
      - .:/app
      - /app/__pycache__
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
    ports:
      - "5678:5678"
    stdin_open: true
    tty: true
```

## 5. Environment Files
**.env.example**
```bash
# Enable debugger (attaches to port 5678)
ENABLE_DEBUG=false
```


# 6. .dockerignore
**gitignore**
```text
__pycache__
*.pyc
.env
.git
.gitignore
README.md
.vscode
.idea
*.log
.DS_Store
scripts/
```

## 7. Usage Commands
```bash
# Normal development (with GUI on Linux)

# Allow Docker containers to access your X11 display
xhost +local:docker

export DISPLAY=$DISPLAY
docker-compose up

# Without GUI (headless test)
docker compose run --rm snake-game python main.py

# With debugger enabled
ENABLE_DEBUG=true docker compose up

# Rebuild after changes
docker compose up --build

# Stop everything
docker compose down

# Quich run docker with rebuild option
./run --rebuild # if requirements.txt and scripts/entrypoint.sh are changed
```
