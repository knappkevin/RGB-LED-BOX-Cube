from adafruit_led_animation.color import RED, GREEN
from collections import deque
import time, random

class Cell:
    def __init__(self, x, y, dir, color):
        self.x = x
        self.y = y
        self.dir = dir
        self.color = color


class Snake:
    def __init__(self, cube, length = 1, delay = 0):
        self.cube = cube
        self.delay = delay
        self.dir_queue = []
        self.ate_apple = False
        self.ate_self = False

        x, y = self.cube.random_cube_xy()
        dir = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.head = Cell(x, y, dir, color = GREEN)

        for cell in range(length):
            x -= dir[0]
            y -= dir[1]

            edgex, edgey, edge_dir = cube.confirm_flat_xy(x, y, dir)
            if edgex != x or edgey != y:
                x, y = edgex, edgey
                dir = -1 * edge_dir[0], -1 * edge_dir[1]
            
            self.dir_queue.insert(0, dir)

        self.tail = Cell(x, y, dir, 0)


    def move_cells(self, head, tail):
        if not self.ate_self:
            # Random chance to turn left or right
            if random.random() < 0.1:
                left_right = random.choice([-1, 1])
                head.dir = (head.dir[1] * left_right, head.dir[0] * left_right)

            # Add the new head direction to the queue
            self.dir_queue.append(head.dir)

            # Move the head and confirm the new position
            head.x += head.dir[0]
            head.y += head.dir[1]

        # Update the tail only if the snake hasn't just eaten
        if not self.ate_apple:
            tail.dir = self.dir_queue.pop(0)  # Get the next direction from the queue
            tail.x += tail.dir[0]
            tail.y += tail.dir[1]
        
        head.x, head.y, head.dir = self.cube.confirm_flat_xy(head.x, head.y, head.dir)
        tail.x, tail.y, tail.dir = self.cube.confirm_flat_xy(tail.x, tail.y, tail.dir)


    def update(self):
        self.move_cells(self.head, self.tail)
        # Check if the head eats an apple, itself, or neither
        reached_color = self.cube.flat_cube_arr[self.head.x][self.head.y]
        self.ate_apple = reached_color == RED
        self.ate_self = reached_color == GREEN

        # Update the position of the head
        if not self.ate_self:
            self.cube.set_pixel(self.head.x, self.head.y, self.head.color)

        # Clear the tail if the snake hasn't just eaten
        if not self.ate_apple:
            self.cube.set_pixel(self.tail.x, self.tail.y, self.tail.color)


    def spawn_apple(self, flat_cube_arr, x, y, spawn_chance):
        # color = self.cube.random_color()
        if random.random() < spawn_chance and flat_cube_arr[x][y] == 0:
            self.cube.set_pixel(x, y, RED)


    def get_name(self):
        return "snake"

    def animate(self, ble_intrrupt):
        apple_spawn_chance = 0.1
        self.cube.function_every_pixel(self.spawn_apple, self.cube.flat_cube_arr, apple_spawn_chance)

        while not ble_intrrupt.in_waiting:
            #spawn a single apple
            x, y = self.cube.random_cube_xy()
            self.spawn_apple(self.cube.flat_cube_arr, x, y, spawn_chance = apple_spawn_chance*2)
            
            self.update() #update snake position and graphics
            self.cube.show_pixels()
            time.sleep(self.delay)
