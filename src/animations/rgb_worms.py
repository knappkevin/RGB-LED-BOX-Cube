import adafruit_fancyled.adafruit_fancyled as fancy
from collections import deque
import time, random
from colors import Colors


class Cell:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

class Worm:
    def __init__(self, cube, x, y, dir, length, color_position, color_step):
        self.cube = cube
        self.length = length
        self.color_step = color_step
        self.head_color_offset = color_position
        self.tail_color_offset = (color_position - (color_step * (length))) % 1 
        self.dir_queue = deque([], length+1)

        self.head = Cell(x, y, dir)

        for cell_number in range(length):
            x -= dir[0]
            y -= dir[1]

            edgex, edgey, edge_dir = cube.confirm_flat_xy(x, y, dir)
            if edgex != x or edgey != y:
                x, y = edgex, edgey
                dir = -1 * edge_dir[0], -1 * edge_dir[1]
            
            self.dir_queue.appendleft(dir)

        self.tail = Cell(x, y, dir)


    def update(self):
        # set and update colors
        head_color = fancy.palette_lookup(Colors.rgb_palette, self.head_color_offset).pack()
        tail_color = fancy.palette_lookup(Colors.rgb_palette, self.tail_color_offset).pack()

        self.cube.set_pixel(self.head.x, self.head.y, head_color)
        # tail should go black or leave another worms color alone
        existing_color = self.cube.flat_cube_arr[self.tail.x][self.tail.y]
        if existing_color == tail_color:
            self.cube.set_pixel(self.tail.x, self.tail.y, 0)

        self.head_color_offset = (self.head_color_offset + self.color_step) % 1
        self.tail_color_offset = (self.tail_color_offset + self.color_step) % 1

        # set and update directions and xy positions
        if random.random() < 0.25:
            left_right = random.choice([-1, 1])
            self.head.dir = (self.head.dir[1] * left_right, self.head.dir[0] * left_right)
        
        self.dir_queue.append(self.head.dir)

        self.head.x += self.head.dir[0]
        self.head.y += self.head.dir[1]

        self.tail.dir = self.dir_queue.popleft()
        self.tail.x += self.tail.dir[0]
        self.tail.y += self.tail.dir[1]

        self.head.x, self.head.y, self.head.dir = self.cube.confirm_flat_xy(self.head.x, self.head.y, self.head.dir)
        self.tail.x, self.tail.y, self.tail.dir = self.cube.confirm_flat_xy(self.tail.x, self.tail.y, self.tail.dir)


"""
example initialization:
rgb_worms = RGBWorms(cube, num_worms=face_width*6, worm_len=1, color_step=0.05, delay=0)

long worm len increases chance of bug
also worms eat their own color
"""
class RGBWorms:
    def __init__(self, cube, num_worms=12//2*6, worm_len=12//2, color_step=0.01, delay=0):
        self.cube = cube
        self.delay = delay
        self.worms = []

        for _ in range(num_worms):
            x, y = cube.random_cube_xy()
            dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            color_position = random.random()
            self.worms.append(Worm(cube, x, y, dir, worm_len, color_position, color_step))

    def get_name(self):
        return "rgb worms"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:

            for worm in self.worms:
                worm.update()
            self.cube.show_pixels()
            time.sleep(self.delay)
