CURRENT_BOT = 4 # 1 = Dumbest, 2 = Common Sense, 3 = Smart, 4 = Smartest
FIRE_RESISTANCE_QUOTIENT = 0.5 # 1 = MOST RESISTANT, 0 = LEAST RESISTANT
TIME_RATE = 0.1 # SECONDS OF WAIT BETWEEN EACH T

GRID_SIZE = 30  # Default value, will update dynamically
MARGIN = 2  # Space between cells
HEADER_HEIGHT = 50  # Space for text and buttons
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 1000  # Default window size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
D1_ORANGE = (255, 140, 0)
D2_ORANGE = (255, 120, 0)
D3_ORANGE = (255, 100, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)

def update_grid_constants(n, screen_width, screen_height):
    global CELL_SIZE, SCREEN_SIZE

    # Ensure cells fit properly within screen dimensions
    max_cell_size_w = (screen_width - (n * MARGIN)) // n
    max_cell_size_h = (screen_height - HEADER_HEIGHT - (n * MARGIN)) // n

    CELL_SIZE = max(5, min(40, min(max_cell_size_w, max_cell_size_h)))  # Keep it reasonable
    SCREEN_SIZE = (n * (CELL_SIZE + MARGIN), n * (CELL_SIZE + MARGIN) + HEADER_HEIGHT)

    return CELL_SIZE, SCREEN_SIZE

# Initialize with default values
CELL_SIZE, SCREEN_SIZE = update_grid_constants(GRID_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT)
