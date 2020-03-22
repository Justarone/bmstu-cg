MAIN_COLOUR = "#4F003C"
ADD_COLOUR = "#FFFFFF"
CANVAS_COLOUR = "#FFFFFF"

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1000

# Frame sizes (relative).
BORDERS_PART = 0.03
BORDERS_WIDTH = int(WINDOW_WIDTH * BORDERS_PART)
BORDERS_HEIGHT = int(WINDOW_HEIGHT * BORDERS_PART)

DATA_PART_WIDTH = 0.28 - 2 * BORDERS_PART
DATA_PART_HEIGHT = 1 - 2 * BORDERS_PART
DATA_WIDTH = int(DATA_PART_WIDTH * WINDOW_WIDTH)
DATA_HEIGHT = int(DATA_PART_HEIGHT * WINDOW_HEIGHT)

FIELD_PART_WIDTH = (1 - DATA_PART_WIDTH) - 4 * BORDERS_PART
FIELD_PART_HEIGHT = 1 - 2 * BORDERS_PART
FIELD_WIDTH = int(FIELD_PART_WIDTH * WINDOW_WIDTH)
FIELD_HEIGHT = int(FIELD_PART_HEIGHT * WINDOW_HEIGHT)
CANVAS_CENTER = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)

FIELD_BORDER_PART = 0.03

INFORMATION = "Information"

ROWS = 23

# INFO_PART_HEIGHT = (1 - DATA_PART_HEIGHT - 2 * BORDERS_PART) - 1 * BORDERS_PART
# INFO_PART_WIDTH = DATA_PART_WIDTH
# INFO_WIDTH = int(INFO_PART_WIDTH * WINDOW_WIDTH)
# INFO_HEIGHT = int(INFO_PART_HEIGHT * WINDOW_HEIGHT)


METHODS = ["ЦДА", "Брезенхем (int)", "Брезенхем (float)", "Брезенхем со сглаживанием",
           "Ву", "Библиотечный"]
COLOURS = ["green", "red", "blue", "black", "white"]
NOM = len(METHODS)

class Colour:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        res = '#'
        res += '0' + hex(self.red)[2:] if self.red < 16 else hex(self.red)[2:]
        res += '0' + hex(self.green)[2:] if self.green < 16 else hex(self.green)[2:]
        res += '0' + hex(self.blue)[2:] if self.blue < 16 else hex(self.blue)[2:]
        return res

    def intensity_apply(self, percent):
        red = int(self.red + (WHITE_COLOUR.red - self.red) * (1 - percent))
        green = int(self.green + (WHITE_COLOUR.green - self.green) * (1 - percent))
        blue = int(self.blue + (WHITE_COLOUR.blue - self.blue) * (1 - percent))
        return Colour(red, green, blue)


class Point:
    def __init__(self, x=0, y=0, colour=Colour()):
        self.x = x
        self.y = y
        self.colour = colour


WHITE_COLOUR = Colour(255, 255, 255)
BLACK_COLOUR = Colour()
GREEN_COLOUR = Colour(green=255)
RED_COLOUR = Colour(red=255)
BLUE_COLOUR = Colour(blue=255)
COLOURS_CODES = [GREEN_COLOUR, RED_COLOUR, BLUE_COLOUR, BLACK_COLOUR, WHITE_COLOUR] 





COEFFS = [0.6, 1, 0.8, 2, 2, 0.8]
