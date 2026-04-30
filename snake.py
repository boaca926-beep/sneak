# from re import S
# from time import sleep

from cmd import PROMPT
from urllib import response

from flask import request
import pygame
import random
import sys
import requests

# Initialize Pygame
pygame.init()

# Constants; game basic attributions
CELL_SIZE = 30  # Size of a single cell
GRID_WIDTH = 20  # Number of grids to width
GRID_HEIGHT = 20  # Number of grids to HEIGHT
WIDTH = GRID_WIDTH * CELL_SIZE  # Total width
HEIGHT = GRID_HEIGHT * CELL_SIZE  # Total HEIGHT
FPS = 5  # Game speed moves per second

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
GRAY = (50, 50, 50)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# API endpoint
API_BASE = "http://localhost:5000"


def random_food_position(snake):
    """
    Generate a radom position that is not occupied by the snake.
    """

    while (
        True
    ):  # Keep creating random food to feed the snake, except interruptions eg., game over, etc.
        x = random.randint(0, GRID_WIDTH - 1)  # Allowed food x coordinates
        y = random.randint(0, GRID_HEIGHT - 1)  # Allowed food y coordinates
        if (x, y) not in snake:
            return (x, y)


def draw_grid(screen):
    """
    Draw grid lines for better visibility.
    """

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_snake(screen, snake):
    """Draw the snake on the screen"""
    for segment in snake:
        rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)
        pygame.draw.rect(screen, DARK_GREEN, rect, 2)  # border
        # print(
        #    f"rec. coord: {segment[0] * CELL_SIZE}, {segment[1] * CELL_SIZE}, {CELL_SIZE}, {CELL_SIZE}"
        # )


def draw_food(screen, food):
    """Draw the food on the screen"""
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, (200, 0, 0), rect, 2)  # border


def show_score(screen, font, score, player_name=""):
    """Display the current score and player name"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    name_text = font.render(f"Player: {player_name}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(name_text, (WIDTH - name_text.get_width() - 10, 10))


def show_game_over(screen, font, score, player_name=""):
    """Display game over message and final score."""
    screen.fill(BLACK)
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
    food = random_food_position(snake)
    score = 0

    return snake, direction, next_direction, food, score


def send_score_to_api(player_name, score):
    """
    Send the final score to the API
    """
    url = f"{API_BASE}/score"
    payload = {"player_name": player_name, "score": score}
    try:
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 201:
            print(f"Score saved: {player_name} - {score}")
        else:
            print(f"Failed to save score: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Error sending score to API: {e}")


# The main program
def main():
    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Get player name
    player_name = get_player_name(screen, font)

    # Game state
    game_over = False
    game_over_sent = False
    snake, direction, next_direction, food, score = reset_game()

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
                print(event.type)

                if not game_over:
                    print("Game ongoing ...")
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
                        print(f"Reset game!")
                        snake, direction, next_direction, food, score = reset_game()
                        game_over = False
                        game_over_sent = False
                    elif event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        sys.exit()

        if not game_over:
            # === Update Game Logic ===
            direction = next_direction  # Apply the queued direction

            # Calculaion new head position
            head_x, head_y = snake[0]
            # print(f"head: (x, y) = ({head_x}, {head_y})")
            dx, dy = direction
            # print(f"(dx, dy) = ({dx}, {dy})")
            new_head = (head_x + dx, head_y + dy)
            # print(f"new head: (x, y) = {new_head}")

            # Check for food collision
            ate_food = new_head == food
            # print(f"ate_food: {ate_food}")

            # print(food)

            # Perform movement
            if ate_food:
                # Insert new head without removing tail (snake grows)
                snake.insert(0, new_head)
                print(f"new head: {new_head}")
                score += 1
                # Generate new food at a position not occupied by the snake
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
            else:
                # Normal move: insert new head and remove tail
                snake.insert(0, new_head)
                snake.pop()

            # === Collision Detection ===
            # Check wall collision
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
            ):
                game_over = True
                continue

            # Check self collision (head colliding with body)
            # print(f"snake: {snake[1:]}, new_head: {new_head}")
            if new_head in snake[1:]:
                game_over = True
                continue

        # === Drawing ===
        screen.fill(BLACK)  # Clear screen
        draw_grid(screen)  # Optional grid
        draw_food(screen, food)  # Draw food
        draw_snake(screen, snake)  # Draw snake
        show_score(screen, font, score, player_name)  # Show score

        if game_over:

            # Use a flag to avoid sending multiple times
            if not game_over_sent:
                send_score_to_api(player_name, score)
                game_over_sent = True
            show_game_over(screen, font, score, player_name)

        pygame.display.flip()  # Update display
        clock.tick(FPS)  # Control game speed

        # continue


if __name__ == "__main__":
    print("Starting tot make a snake game ...")
    main()
