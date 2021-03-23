import pyautogui

_, SCREEN_HEIGHT = pyautogui.size()
BOARD_SIZE = SCREEN_HEIGHT * 2/3

# Boids attributes
PERCEPTION = SCREEN_HEIGHT / 8
MAX_SPEED = 8
MAX_FORCE = 0.5

COLOUR_RED = "red"
COLOUR_WHITE = "white"
COLOUR_GREY = "gray64"
COLOUR_ORANGE = "DarkOrange1"
COLOUR_CORAL = "coral"