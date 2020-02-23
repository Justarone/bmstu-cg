MAIN_COLOUR = "#16471d"
ADD_COLOUR = "#f1ffe8"

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800

# Frame sizes (relative).
BORDERS_PART = 0.03
BORDERS_WIDTH = int(WINDOW_WIDTH * BORDERS_PART)
BORDERS_HEIGHT = int(WINDOW_HEIGHT * BORDERS_PART)

DATA_PART_WIDTH = 0.25 - 2 * BORDERS_PART
DATA_PART_HEIGHT = 1 - 2 * BORDERS_PART
DATA_WIDTH = int(DATA_PART_WIDTH * WINDOW_WIDTH)
DATA_HEIGHT = int(DATA_PART_HEIGHT * WINDOW_HEIGHT)

FIELD_PART_WIDTH = 0.75 - 2 * BORDERS_PART
FIELD_PART_HEIGHT = 1 - 2 * BORDERS_PART
FIELD_WIDTH = int(FIELD_PART_WIDTH * WINDOW_WIDTH)
FIELD_HEIGHT = int(FIELD_PART_HEIGHT * WINDOW_HEIGHT)

POINT_SIZE = 2

FIELD_BORDER_PART = 0.03

INFORMATION = '''
Here should be info...
'''

SCALE = 10
MAX_LIMIT_X = FIELD_WIDTH // SCALE
MAX_LIMIT_Y = FIELD_HEIGHT // SCALE // 2
MIN_LIMIT_X = 0
MIN_LIMIT_Y = -MAX_LIMIT_Y
