import time
import adafruit_fancyled.adafruit_fancyled as fancy

class RGBWave:
    def __init__(self, cube, step_size=0.03):
        self.cube = cube
        self.step_size = step_size
        self.face_num_leds = cube.face_width * cube.face_width

        # Declare a 6-element RGB rainbow palette
        self.palette = [
            fancy.CRGB(0.5, 0.0, 0.0),  # Red
            fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
            fancy.CRGB(0.0, 0.5, 0.0),  # Green
            fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
            fancy.CRGB(0.0, 0.0, 0.5),  # Blue
            fancy.CRGB(0.5, 0.0, 0.5),  # Magenta
        ]

        self.pixels_top = self.cube.pixels_top
        self.pixels_bottom = self.cube.pixels_bottom
        self.pixels_sides = self.cube.pixels_sides
        self.offset = 0  # Positional offset into color palette to get it to 'spin'

    def get_name(self):
        return "rgb wave"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:
            for i in range(self.face_num_leds): # for all faces
                color = fancy.palette_lookup(self.palette, self.offset + i / (self.face_num_leds * 3))
                color = color.pack()
                self.cube.pixels_sides[i] = color
                self.cube.pixels_top[i] = color
                self.cube.pixels_bottom[i] = color

            for i in range(self.face_num_leds, self.face_num_leds*4): # for the remaining 3 side faces
                # Load each pixel's color from the palette using an offset, run it
                # through the gamma function, pack RGB value and assign to pixel.
                color = fancy.palette_lookup(self.palette, self.offset + i / (self.face_num_leds * 3))
                color = color.pack()
                self.cube.pixels_sides[i] = color

            self.offset = (self.offset + self.step_size) % 1 # Bigger added number = faster spin

            self.cube.show_pixels()
