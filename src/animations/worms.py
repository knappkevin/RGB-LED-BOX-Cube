from collections import deque
import time, random

class Cell:
    def __init__(self, x, y, dir, color):
        self.x = x
        self.y = y
        self.dir = dir
        self.color = color


class Worm:
    def __init__(self, cube, x, y, dir, length, color):
        self.cube = cube
        self.length = length
        self.dir_queue = deque([], length+1)

        self.head = Cell(x, y, dir, color)

        for cell_number in range(length):
            x -= dir[0]
            y -= dir[1]

            edgex, edgey, edge_dir = cube.confirm_flat_xy(x, y, dir)
            if edgex != x or edgey != y:
                x, y = edgex, edgey
                dir = -1 * edge_dir[0], -1 * edge_dir[1]
            
            self.dir_queue.appendleft(dir)

        self.tail = Cell(x, y, dir, 0)


    def update(self):
        self.cube.set_flat_cube_pixel(self.head.x, self.head.y, self.head.color)
        # tail should go black or leave another worms color alone
        existing_color = self.cube.flat_cube_arr[self.tail.x][self.tail.y]
        if existing_color == self.head.color:
            self.cube.set_flat_cube_pixel(self.tail.x, self.tail.y, 0)
        else:
            self.cube.set_flat_cube_pixel(self.tail.x, self.tail.y, existing_color)

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
example usage:
worms = Worms(cube, num_worms=30, worm_len=face_width//2, delay=0)
worms.animate()

long worm len increases chance of bug
also worms eat their own color
"""
class Worms:
    def __init__(self, cube, num_worms, worm_len, delay):
        self.cube = cube
        self.delay = delay
        self.worms = []

        for _ in range(num_worms):
            color = cube.random_color()
            dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            x = random.randint(0, cube.face_width - 1)
            y = random.randint(0, cube.face_width - 1)
            face = random.choice([cube.TOP, cube.BOTTOM, cube.SIDE_A, cube.SIDE_B, cube.SIDE_C, cube.SIDE_D])
            flatx, flaty = cube.get_flat_cube_xy(face, x, y)
            
            self.worms.append(Worm(cube, flatx, flaty, dir, worm_len, color))

    def get_name(self):
        return "worms"

    def animate(self, ble_intrrupt):
        while not ble_intrrupt.in_waiting:            
            for worm in self.worms:
                worm.update()
            self.cube.show_pixels()
            time.sleep(self.delay)
