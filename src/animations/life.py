import random, time
from colors import Colors

class Life:
    def __init__(self, cube, pop_density, delay):
        self.cube = cube
        self.pop_density = pop_density
        self.delay = delay
        self.flatCubeArr1 = cube.instantiate_arr(cube.face_width)
        self.flatCubeArr2 = cube.instantiate_arr(cube.face_width)
        # self.cube.function_every_pixel(self.populate_pixel, self.flatCubeArr1, pop_density)
        self.NEIGHBOR_OFFSETS = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),          (1, 0),
            (-1, -1), (0, -1), (1, -1)]


    def populate_pixel(self, flatCubeArr, x, y, pop_density):
        color = Colors.random_color()
        if random.random() < pop_density:
            flatCubeArr[x][y] = color


    def life_rule_on_cell(self, new, x, y, old):
        # Process neighbors and count races
        neighbor_count = 0
        races = {}

        for dx, dy in self.NEIGHBOR_OFFSETS:
            nx, ny = x + dx, y + dy
            # Confirm and adjust coordinates for wrap-around
            nx, ny, _ = self.cube.confirm_flat_xy(nx, ny, None)
            if nx is None: continue
            
            # Get the neighbor value directly from the old array
            neighbor_val = old[nx][ny]
            
            # Skip dead neighbors
            if neighbor_val != 0:
                neighbor_count += 1
                if neighbor_val in races:
                    races[neighbor_val] += 1 # Increment race count
                else:
                    races[neighbor_val] = 1 # Initialize race count

        # Apply Game of Life rules
        current_val = old[x][y]
        
        if current_val == 0 and neighbor_count == 3:
            # Birth: The cell is dead but has exactly 3 live neighbors
            # Find the race with the most neighbors
            new[x][y] = max(races, key=races.get)
        elif neighbor_count < 2 or neighbor_count > 3:
            # Death: The cell is alive but has less than 2 or more than 3 neighbors
            new[x][y] = 0
        else:
            # Survival: Keep the current state
            new[x][y] = current_val


    def get_name(self):
        return "life"

    def animate(self, ble_intrrupt):
        self.cube.function_every_pixel(self.populate_pixel, self.flatCubeArr1, self.pop_density)
        self.cube.set_pixels()
        self.cube.show_pixels()

        while not ble_intrrupt.in_waiting:
            self.cube.function_every_pixel(self.life_rule_on_cell, self.flatCubeArr2, self.flatCubeArr1)
            self.cube.flat_cube_arr = self.flatCubeArr2
            self.cube.set_pixels()
            self.cube.show_pixels()
            # time.sleep(self.delay)

            self.cube.function_every_pixel(self.life_rule_on_cell, self.flatCubeArr1, self.flatCubeArr2)
            self.cube.flat_cube_arr = self.flatCubeArr1
            self.cube.set_pixels()
            self.cube.show_pixels()
            # time.sleep(self.delay)