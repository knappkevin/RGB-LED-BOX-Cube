import adafruit_fancyled.adafruit_fancyled as fancy

class RGBFill:
    def __init__(self, cube, step_size = 0.02):
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
        return "rgb fill"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:

            color = fancy.palette_lookup(self.palette, self.offset)
            color = color.pack()
            self.cube.fill_pixels(color)

            self.offset = (self.offset + self.step_size) % 1

            self.cube.show_pixels()
