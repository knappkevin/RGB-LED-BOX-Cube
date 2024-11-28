import random, time
from colors import Colors

class Line:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

class Test:
    def __init__(self, cube):
        self.cube = cube
        qrtpt = cube.face_width // 4
        thirdqrtpt = 3 * qrtpt

        x1, y1 = cube.get_flat_cube_xy(cube.TOP, qrtpt, qrtpt)
        x2, y2 = cube.get_flat_cube_xy(cube.SIDE_A, qrtpt, qrtpt)
        x3, y3 = cube.get_flat_cube_xy(cube.SIDE_D, qrtpt, qrtpt)

        self.lines = []
        self.lines.append(Line(x1, y1, (1, 0)))
        self.lines.append(Line(x2, y2, (0, -1)))
        self.lines.append(Line(x3, y3, (-1, 0)))

        x4, y4 = cube.get_flat_cube_xy(cube.TOP, thirdqrtpt, thirdqrtpt)
        x5, y5 = cube.get_flat_cube_xy(cube.SIDE_A, thirdqrtpt, thirdqrtpt)
        x6, y6 = cube.get_flat_cube_xy(cube.SIDE_D, thirdqrtpt, thirdqrtpt)

        self.lines.append(Line(x4, y4, (-1, 0)))
        self.lines.append(Line(x5, y5, (0, 1)))
        self.lines.append(Line(x6, y6, (1, 0)))

    def update_line(self, line):
        self.cube.set_pixel(line.x, line.y, Colors.random_color())
        line.x += line.dir[0]
        line.y += line.dir[1]
        line.x, line.y, line.dir = self.cube.confirm_flat_xy(line.x, line.y, line.dir)

    def get_name(self):
        return "test"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:            
            for line in self.lines:
                self.update_line(line)
            self.cube.show_pixels()