import webbrowser
import os
from collections import deque # for BFS, FS stands for Breadth-First Search - it's a graph traversal algorithm that explores nodes level by level, moving outward from the starting point.
import pygame
import random
import sys
import requests
from helper import create_beep_sounds

# Initialize Pygame
pygame.init()

# Initialize font system
pygame.font.init()

# Initialize sound mixer (THIS IS CRITICAL!)
pygame.mixer.init()

# Create sound files if they don't exist
create_beep_sounds()

# Initialize sound (add this after pygame.init())
try:
    eat_sound = pygame.mixer.Sound("./music/eat.wav")
    game_over_sound = pygame.mixer.Sound("./music/game_over.wav")
except:
    print("Sound files not found, playing without sound")
    eat_sound = None
    game_over_sound = None

# Load and play background music
bkg_music=f"./music/background_rock"
try:
    if os.path.exists(f"{bkg_music}.mp3"):
        pygame.mixer.music.load(f"{bkg_music}.mp3")
        pygame.mixer.music.set_volume(0.3)  # 30% volume
        pygame.mixer.music.play(-1)  # Loop forever
        print("🎵 Background music playing")
    else:
        print("⚠️ No background.wav found")
except Exception as e:
    print(f"⚠️ Could not play background music: {e}")



# ========================== GAME MODES ==========================
#global vs_ai # Set to True for Human vs AI, False for single‑player
#vs_ai = select_game_mode(screen, font)
# ================================================================

# Constants; game basic attributions
CELL_SIZE = 30  # Size of a single cell
GRID_WIDTH = 20  # Number of grids to width
GRID_HEIGHT = 20  # Number of grids to HEIGHT
WIDTH = GRID_WIDTH * CELL_SIZE  # Total width
HEIGHT = GRID_HEIGHT * CELL_SIZE  # Total HEIGHT

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 0)  # Human snake color
BLUE = (0, 0, 200)  # AI snake color
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

# Level progression
LEVEL_EVERY = 5  # Increase level every N points


def random_food_position(snake, snake2=None):
    """
    Generate a radom position that is not occupied by any snake.
    """

    while (
        True
    ):  # Keep creating random food to feed the snake, except interruptions eg., game over, etc.
        x = random.randint(0, GRID_WIDTH - 1)  # Allowed food x coordinates
        y = random.randint(0, GRID_HEIGHT - 1)  # Allowed food y coordinates
        if (x, y) not in snake and (snake2 is None or (x, y) not in snake2):
            return (x, y)


def draw_grid(screen):
    """
    Draw grid lines for better visibility.
    """

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_snake(screen, snake, color, border_color):
    """Draw the snake on the screen"""
    for segment in snake:
        rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, border_color, rect, 2)  # border
        # print(
        #    f"rec. coord: {segment[0] * CELL_SIZE}, {segment[1] * CELL_SIZE}, {CELL_SIZE}, {CELL_SIZE}"
        # )


def draw_food(screen, food):
    """Draw the food on the screen"""
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, (200, 0, 0), rect, 2)  # border


def show_score(screen, font, score, player_name="", level=1, x=10, y=10):
    """Display score for a player (default top‑left)."""
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    name_text = font.render(f"{player_name}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (x, y))
    screen.blit(name_text, (x, y + 30))
    screen.blit(level_text, (x, y + 60))


def show_game_over(screen, font, score, player_name="", winner=None):
    """Display game over message and final score."""
    screen.fill(BLACK)
    if winner:
        game_over_text = font.render(f"{winner} WINS!", True, RED)
    else:
        game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    name_text = font.render(f"Player: {player_name}", True, WHITE)

    # Center the message
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()


def show_paused(screen, font):
    """Display paused message."""
    paused_text = font.render("PAUSED", True, WHITE)
    resume_text = font.render("Press any key to resume", True, WHITE)  # <-- updated message
    screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()


def get_player_name(screen, font):
    """Get player name before game starts."""
    name = ""
    input_active = True
    cursor_visible = True
    cursor_timer = 0

    prompt_text = font.render("Enter your name: ", True, WHITE)
    instruction_text = font.render("Press Enter to start, ESC to default", True, GRAY)

    while input_active:
        screen.fill(BLACK)

        # Draw title
        title_text = font.render("SNAKE GAME", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 150))

        # Draw prompt
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 50))

        # Draw name input with blinking cursor
        display_name = name
        if cursor_visible:
            display_name += "_"
        name_surface = font.render(display_name, True, GREEN)
        screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, HEIGHT // 2))

        # Draw instruction
        screen.blit(
            instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 80)
        )

        pygame.display.flip()

        # Blinking cursor (every 30 frames)
        cursor_timer += 1
        if cursor_timer >= 300:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # input_active = False
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name:
                        input_active = False
                    elif not name:
                        name = "Player"  # Default if no name entered
                        input_active = False

                elif event.key == pygame.K_ESCAPE:
                    name = "Player"
                    input_active = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    # Allow letters, number, and spaces (max 15 chars)
                    if len(name) < 15 and event.unicode.isprintable() and event.unicode != "":
                        name += event.unicode

    return name if name else "Player"


def reset_game():
    """Reset game variables for a new round."""
    # Initial snake: three cells in the middle, movin right
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
    Avoid walls, own body, and the other snake's body
    Returns a safe direction (UP/DOWN/LEFT/RIGHT)
    """
    head = snake[0]
    grid_w, grid_h = GRID_WIDTH, GRID_HEIGHT

    # Blocked cells: own body (expect tail will move, but we include it for safty)
    blocked = set(snake[1:])
    if other_snake is not None:
        blocked.update(other_snake) # avoid hitting the other snake by adding the other snake's body

    queue = deque([(head, [])]) # Start with head position and empty path
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

    # No path found -> pick a safe move that does not ause immediate death
    for direction, (dx, dy) in dirs:
        nx, ny = head[0] + dx, head[1] + dy
        if 0 <= nx < grid_w and 0 <= ny < grid_h:
            if (nx, ny) not in snake[1:]:
                if other_snake is None or (nx, ny) not in other_snake:
                    return direction
    return UP # fallback

def send_score_to_api(player_name, score, level):
    url = f"{API_BASE}/score"
    payload = {"player_name": player_name, "score": int(score), "level": level}
    try:
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 201:
            print(f"Score saved: {player_name} - {score} (level {level})")
        else:
            print(f"Failed to save score: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Error sending score to API: {e}")

def select_game_mode(screen, font):
    """Allow player to select game mode at startup."""
    options = ["Single Player", "VS AI"]
    selected = 0

    while True:
        screen.fill(BLACK)

        # Draw title
        title_text = font.render("SNAKE GAME", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 150))
        
        # Draw instruction
        instruction_text = font.render("Select Game Mode:", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 80))

        # Draw options
        for i, option in enumerate(options):
            color = BLUE if i == selected else WHITE
            mode_text = font.render(option, True, color)
            y_pos = HEIGHT // 2 -20 + (i * 60)
            screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, y_pos))

        # Draw controls
        controls_text = font.render("Use UP/DOWN to select, ENTER to confirm", True, GRAY)
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                    #print(selected, selected - 1)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    # Return True for VS AI mode, False for single player
                    return selected == 1

    #return False

# The main program
def main():
    global FPS, vs_ai

    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Select game mode
    #vs_ai = False
    vs_ai = select_game_mode(screen, font)

    # Get player name
    player_name = get_player_name(screen, font)

    # Difficult selection
    print("\nChoose difficulty level: 1=Easy (slow), 2=Medium (Medium), 3=Hard (fast)")
    diff = "1"  # input("Enter 1, 2 or 3 (default=2): ") or "2"
    base_fps = {"1": 4, "2": 10, "3": 14}.get(diff, 10)
    FPS = base_fps
    MAX_FPS = base_fps + 5  # so hard starts faster and can go even higher
    starting_fps = FPS  # Store initial FPS for reference
    SPEED_INCREMENT = 0.5  # Increase FPS by this amount for every 2.5 points scored
    INCREMENT_EVERY = 3  # Increase speed every N foods eaten

    # Webbrowser – gracefully handle absence
    leaderboard_url = "http://localhost:5000/leaderboard"
    try:
        # Only attempt if DISPLAY is set (X11 available for pygame)
        if os.environ.get("DISPLAY"):
            webbrowser.open(leaderboard_url)
        else:
            print("No DISPLAY set – skipping automatic browser open.")
    except Exception as e:
        print(f"Browser open skipped (Docker environment): {e}")

    # Game state (signal or two-player)
    game_over = False
    game_over_sent = False
    paused = False

    # Human player (always present)
    snake, direction, next_direction, score = reset_game()
    level = 1

    # AI oppenent (only if vs_ai is True)
    if vs_ai:
        snake_ai, direction_ai, next_direction_ai, score_ai = reset_ai_snake()
        level_ai = 1
        print("AI opponent enabled!")
    else:
        snake_ai = None
        direction_ai = None
        next_direction_ai = None
        score_ai = 0
        level_ai = 0
        print("Playing against yourself! (no AI opponent)")

    # Initial food (no collision)
    food = random_food_position(snake, snake_ai)

    winner = None  # Track winner for potential future use
    running = True

    while running:
        # === Event Handling ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Here we quit!")
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #print(event.type)

                if not game_over:
                    # print("Game ongoing ...")
                    if not paused:
                        # Normal gameplay: change direction or pause
                        if event.key == pygame.K_UP and direction != DOWN:
                            next_direction = UP
                        elif event.key == pygame.K_DOWN and direction != UP:
                            next_direction = DOWN
                        elif event.key == pygame.K_LEFT and direction != RIGHT:
                            next_direction = LEFT
                        elif event.key == pygame.K_RIGHT and direction != LEFT:
                            next_direction = RIGHT
                        elif event.key == pygame.K_p:
                            paused = True  # Pause the game
                    else:
                        # Game is paused: any key press resumes
                        # (except we still allow Q to quit if desired)
                        if event.key == pygame.K_q:
                            running = False
                            pygame.quit()
                            sys.exit()
                        else:
                            paused = False  # Resume on any other key
                else:
                    # When game over, check for restart or quit
                    if event.key == pygame.K_r:
                        # Reset everything
                        print(f"Reset game!")
                        snake, direction, next_direction, score = reset_game()
                        level = 1
                        if vs_ai:
                            snake_ai, direction_ai, next_direction_ai, score_ai = reset_ai_snake()
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

        # ========== PAUSE HANDLING ==========
        # If paused, draw everything but skip game logic
        if paused and not game_over:
            screen.fill(BLACK)
            draw_grid(screen)
            draw_food(screen, food)
            draw_snake(screen, snake, GREEN, DARK_GREEN)
            if vs_ai:
                draw_snake(screen, snake_ai, BLUE, DARK_BLUE)
            show_score(screen, font, score, player_name, level, 10, 10)
            if vs_ai:
                show_score(screen, font, score_ai, "AI", level_ai, WIDTH - 150, 10)
            show_paused(screen, font)
            pygame.display.flip()
            clock.tick(FPS)
            continue  # Do not update game state

        # === Update Game Logic ===
        if not game_over:
            # === Human snake movement ===
            direction = next_direction  # Apply the queued direction

            # Calculaion new head position
            head_x, head_y = snake[0]
            # print(f"head: (x, y) = ({head_x}, {head_y})")
            dx, dy = direction
            # print(f"(dx, dy) = ({dx}, {dy})")
            new_head = (head_x + dx, head_y + dy)
            # print(f"new head: (x, y) = {new_head}")

            # === AI snake movement (if vs_ai is true)
            if vs_ai:
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



            # Check for food collision
            ate_food = new_head == food
            ate_food_ai = (vs_ai and new_head_ai == food)
            # print(f"ate_food: {ate_food}")
            any_ate = ate_food or ate_food_ai

            # Play sound when eating
            if ate_food and eat_sound:
                eat_sound.play()
            elif ate_food_ai and eat_sound:
                eat_sound.play()

            # Human movement
            if ate_food:
                # Insert new head without removing tail (snake grows)
                snake.insert(0, new_head)
                # print(f"new head: {new_head}")
                score += 1  # Increase score by 1.5 for each food eaten

                # Level progession
                new_level = int(score) // LEVEL_EVERY + 1
                if new_level > level:
                    level = new_level
                    print(f"⭐ Level up! Now level {level}")
                    # Optional: increase speed on level up
                    FPS = min(MAX_FPS, FPS + SPEED_INCREMENT)
                    print(f"Speed increased! Current FPS: {FPS}")
            else:
                # Normal move: insert new head and remove tail
                snake.insert(0, new_head)
                snake.pop()

            # Handle AI eating
            if vs_ai:
                if ate_food_ai:
                    snake_ai.insert(0, new_head_ai)
                    score_ai += 1  # Changed from 1.5 to 1
                    new_level_ai = int(score_ai) // LEVEL_EVERY + 1
                    if new_level_ai > level_ai:
                        level_ai = new_level_ai
                else:
                    # Normal move for AI
                    snake_ai.insert(0, new_head_ai)
                    snake_ai.pop()
        
            # Generate new food at a position not occupied by the snake
            if any_ate:
                # Find all free cells
                if vs_ai:
                    free_cells = [
                        (x, y)
                        for x in range(GRID_WIDTH)
                        for y in range(GRID_HEIGHT)
                        if (x, y) not in snake and (x, y) not in snake_ai
                    ]
                else:
                    free_cells = [
                        (x, y)
                        for x in range(GRID_WIDTH)
                        for y in range(GRID_HEIGHT)
                        if (x, y) not in snake
                    ]

                if not free_cells:
                    # Snake has filled the grid - player wins
                    game_over = True
                    continue
                food = random.choice(free_cells)
            

            # === Collision Detection ===
            # Check wall collision
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
            ):
                if game_over_sound:
                    game_over_sound.play()
                game_over = True
                winner = "Human (Wall)"
                continue

            # Check self collision (head colliding with body)
            # print(f"snake: {snake[1:]}, new_head: {new_head}")
            if new_head in snake[1:]:
                if game_over_sound:
                    game_over_sound.play()
                game_over = True
                winner = "Human (Self)"
                continue

            # AI collision checks (only if vs_ai is True)
            if vs_ai:
                # Check AI self collision
                if new_head_ai in snake_ai[1:]:
                    if game_over_sound:
                        game_over_sound.play()
                    game_over = True
                    winner = "AI (Self)"
                    continue

                # Check human head vs AI body
                if new_head in snake_ai:
                    if game_over_sound:
                        game_over_sound.play()
                    game_over = True
                    winner = "AI"
                    continue

                # Check AI head vs human body
                if new_head_ai in snake:
                    if game_over_sound:
                        game_over_sound.play()
                    game_over = True
                    winner = "Human"
                    continue

                # Check head-on collision (both heads same cell)
                if new_head == new_head_ai:
                    if game_over_sound:
                        game_over_sound.play()
                    game_over = True
                    winner = "Tie!"
                    continue

        # === Drawing ===
        screen.fill(BLACK)  # Clear screen
        draw_grid(screen)  # Optional grid
        draw_food(screen, food)  # Draw food
        draw_snake(screen, snake, GREEN, DARK_GREEN)  # Draw snake
        if vs_ai:
            draw_snake(screen, snake_ai, BLUE, DARK_BLUE)

        # Display scores and level
        show_score(screen, font, score, player_name, level, 10, 10)
        if vs_ai:
            show_score(screen, font, score_ai, "AI", level_ai, WIDTH - 150, 10)

        if game_over:
            # Use a flag to avoid sending multiple times
            if not game_over_sent:
                send_score_to_api(player_name, int(score), level)
                game_over_sent = True
            show_game_over(screen, font, score, player_name)
        elif paused:
            # Extra safety (should already be handled above)
            show_paused(screen, font)

        pygame.display.flip()  # Update display
        clock.tick(FPS)  # Control game speed


if __name__ == "__main__":
    print("Starting to make a snake game ...")
    main()
