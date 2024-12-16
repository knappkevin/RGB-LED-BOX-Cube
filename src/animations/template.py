import time

class Template:
    def __init__(self, cube, delay=0):
        self.cube = cube
        self.delay = delay

    def foo(self):
        return

    def get_name(self):
        return "template"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:

            self.foo()
            self.cube.show_pixels()
            time.sleep(self.delay)