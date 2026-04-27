#import pygame
#import random

# Initialize Pygame
#pygame.init()

# Constants; game basic attributions
CELL_SIZE = 30      # Size of a single cell
GRID_WIDTH = 20     # Number of grids to width
GRID_HEIGHT = 20    # Number of grids to height  
WIDTH = GRID_WIDTH * CELL_SIZE  # Total width
HIGHT = GRID_HEIGHT * CELL_SIZE # Total hight
FPS = 10 # Game speed moves per second

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

def random_food_position(snake):
    """
    Generate a radom position that is not occupied by the snake.
    """

    while True: # Keep creating random food to feed the snake, except interruptions eg., game over, etc.
        x = random.radint(0, GRID_WIDTH - 1) # Allowed food x coordinates
        y = random.radint(0, GRID_HEIGHT - 1) # Allowed food y coordinates  
        if (x, y) not in snake:
            return (x, y)

if __name__ == "__main__":
    print("Starting tot make a snake game ...")
