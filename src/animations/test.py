from adafruit_led_animation.color import RED, GREEN, TEAL, AQUA, CYAN, BLUE, PURPLE, MAGENTA

# for all faces on each led strip, identify the first pixels with green and the last pixels with red, otherwise blue
class Test:
    def __init__(self, cube):
        self.cube = cube
        self.face_num_leds = cube.face_width * cube.face_width
        self.pixels_top = self.cube.pixels_top
        self.pixels_bottom = self.cube.pixels_bottom
        self.pixels_sides = self.cube.pixels_sides


    def identify_pixels(self, strip, faces):
        strip.fill(BLUE)
        for face in range(faces):

            start = face * self.face_num_leds
            strip[start] = GREEN
            strip[start + 1] = GREEN

            end = (face+1) * self.face_num_leds - 1
            strip[end] = RED
            strip[end - 1] = RED


    def get_name(self):
        return "test"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:

            self.identify_pixels(self.pixels_top, 1)
            self.identify_pixels(self.pixels_sides, 4)
            self.identify_pixels(self.pixels_bottom, 1)
            self.cube.show_pixels()