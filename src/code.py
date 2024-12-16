import board

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from cube import LEDCube
from controller import AnimationController

from animations.test import Test
from animations.worms import Worms
from animations.rgb_worms import RGBWorms
from animations.rgb_fleas import RGBFleas
from animations.life import Life
from animations.life_alternative import LifeAlternative
from animations.snake import Snake
from animations.rgb_wave import RGBWave
from animations.rgb_fill import RGBFill
from animations.rgb_pulse import RGBPulse


# Define face dimensions
face_width = 16

"""
Initialize the cube
brightness recommended between 0.03 and 0.1 depending
"""
cube = LEDCube(face_width, board.IO1, board.IO2, board.IO3, brightness=0.05)

# Initialize animations
test = Test(cube)
worms = Worms(cube, num_worms=face_width//2*6, worm_len=face_width//2, delay=0)
rgb_worms = RGBWorms(cube, num_worms=face_width//2*6, worm_len=face_width//2, color_step=0.01, delay=0)
rgb_fleas = RGBFleas(cube, num_fleas=face_width*6, color_step=0.03, delay=0)
life = Life(cube, pop_density=0.2, delay=0)
life_alt = LifeAlternative(cube, pop_density=0.10, delay=0)
snake = Snake(cube, delay=0.01)
rgb_wave = RGBWave(cube, step_size=0.03)
rgb_fill = RGBFill(cube, step_size=0.02)
rgb_pulse = RGBPulse(cube, brightness_step=0.1)

# Advertise bluetooth low energy uart service
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.start_advertising(advertisement)

# Handle animations and user requests
controller = AnimationController(rgb_wave, rgb_fill, rgb_pulse, rgb_fleas, rgb_worms, worms, snake, life, test)
controller.run(cube, uart)