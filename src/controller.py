class AnimationController:
    def __init__(self, *animations):
        self.animations = {ani.get_name(): ani for ani in animations}
        self.animation = animations[0]

    def write_line(self, uart, msg):
        uart.write(msg + '\n')

    def run(self, cube, uart):
        self.animation.animate(uart)

        while True:
            if uart.in_waiting: # new line of data is available to read
                data = uart.readline().decode('utf-8').strip()

                if data in self.animations:
                    clear_pixel = lambda arr, x, y: cube.set_pixel(x, y, 0)
                    cube.function_every_pixel(clear_pixel, cube.flat_cube_arr)
                    cube.fill_pixels(0)
                    self.animation = self.animations[data]
                else:
                    self.write_line(uart, 'Available animations:')
                    self.write_line(uart, ', '.join(self.animations.keys()))
                
                self.write_line(uart, 'Running ' + self.animation.get_name())
                self.animation.animate(uart)
