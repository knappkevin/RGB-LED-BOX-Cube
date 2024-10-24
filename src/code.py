from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import board
from cube import LEDCube
from controller import AnimationController

from animations.test import Test
from animations.worms import Worms
from animations.life import Life


# Define face dimensions
face_width = 16

"""
Initialize the cube
brightness recommended between 0.03 and 0.1 depending
"""
cube = LEDCube(face_width, board.A0, board.A1, board.A2, brightness=0.03)

# Initialize animations
test = Test(cube)
worms = Worms(cube, num_worms=36, worm_len=face_width//2, delay=0)
life = Life(cube, pop_density=0.2, delay=0)

# Advertise bluetooth low energy uart service
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.start_advertising(advertisement)

# Handle animations and user requests
controller = AnimationController(test, worms, life)
controller.run(cube, uart)
