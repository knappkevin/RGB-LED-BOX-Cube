import adafruit_fancyled.adafruit_fancyled as fancy
import time, random
from colors import Colors

class Flea:
    def __init__(self, cube, x, y, dir, color_position, color_step):
        self.cube = cube
        self.color_step = color_step
        self.color_offset = color_position
        self.x = x
        self.y = y
        self.dir = dir

    def update(self):
        # set and update colors
        flea_color = fancy.palette_lookup(Colors.rgb_palette, self.color_offset).pack()
        self.cube.set_pixel(self.x, self.y, flea_color)
        self.color_offset = (self.color_offset + self.color_step) % 1

        # set and update directions and xy positions
        if random.random() < 0.5:
            self.dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        
        self.x += self.dir[0]
        self.y += self.dir[1]
        self.x, self.y, self.dir = self.cube.confirm_flat_xy(self.x, self.y, self.dir)


"""
example usage:
rgb_fleas = RGBFleas(cube, num_fleas=face_width*6, color_step=0.03, delay=0)
rgb_fleas.animate()

long worm len increases chance of bug
also fleas eat their own color
"""
class RGBFleas:
    def __init__(self, cube, num_fleas=12*6, color_step=0.03, delay=0):
        self.cube = cube
        self.delay = delay
        self.fleas = []

        for _ in range(num_fleas):
            x, y = cube.random_cube_xy()
            dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            color_position = random.random()
            self.fleas.append(Flea(cube, x, y, dir, color_position, color_step))

    def get_name(self):
        return "rgb fleas"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:

            self.cube.fill_pixels(0)
            for flea in self.fleas:
                flea.update()
            self.cube.show_pixels()
            time.sleep(self.delay)
 