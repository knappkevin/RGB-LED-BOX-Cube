from colors import Colors

class RGBPulse:
    def __init__(self, cube, brightness_step=0.1):
        self.cube = cube
        self.color_index = 0
        self.colors = Colors.color_list
        self.color = self.colors[self.color_index]
        
        self.brightness = 0 # value between 0 and 1
        self.brightness_step = brightness_step # step size for brightness
        self.increasing = True

    def get_name(self):
        return "rgb pulse"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:
            # Update brightness
            if self.increasing:
                self.brightness += self.brightness_step
                if self.brightness >= 1:
                    self.brightness = 1
                    self.increasing = False
            else:
                self.brightness -= self.brightness_step
                if self.brightness <= 0:
                    self.brightness = 0
                    self.increasing = True
                    self.color_index += 1 # get next color from list
                    self.color = self.colors[self.color_index % len(self.colors)]

            # Scale the color by the brightness
            scaled_color = tuple(int(c * self.brightness) for c in self.color)

            # Set the color for all pixels
            self.cube.fill_pixels(scaled_color)

            # Update the display
            self.cube.show_pixels()