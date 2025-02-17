FIRE_RESISTANCE_QUOTIENT = 0 # 1 = MOST RESISTANT, 0 = LEAST RESISTANT

GRID_SIZE = 40  # Default value, will update dynamically
MARGIN = 2  # Space between cells
HEADER_HEIGHT = 50  # Space for text and buttons
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800  # Default window size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
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
