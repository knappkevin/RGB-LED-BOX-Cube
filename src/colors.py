import random
from adafruit_led_animation.color import RED, ORANGE, AMBER, YELLOW, GOLD, GREEN, JADE, TEAL, AQUA, CYAN, BLUE, PURPLE, MAGENTA, PINK, WHITE
import adafruit_fancyled.adafruit_fancyled as fancy


class Colors:
    color_list = [RED, ORANGE, AMBER, YELLOW, GOLD, GREEN, JADE, TEAL, AQUA, CYAN, BLUE, PURPLE, MAGENTA, PINK]

    rgb_palette = [
        fancy.CRGB(0.5, 0.0, 0.0),  # Red
        fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
        fancy.CRGB(0.0, 0.5, 0.0),  # Green
        fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
        fancy.CRGB(0.0, 0.0, 0.5),  # Blue
        fancy.CRGB(0.5, 0.0, 0.5),  # Magenta
    ]


    def random_color():
        colors = [RED, ORANGE, AMBER, YELLOW, GOLD, GREEN, JADE, TEAL, AQUA, CYAN, BLUE, PURPLE, MAGENTA, PINK, WHITE]
        return random.choice(colors)

