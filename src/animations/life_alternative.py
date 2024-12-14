import random, time
from colors import Colors

'''
variation of the life animation that has a faster best case scenario on low populations but
has a slower worst case scenario and suffers on memory
'''
class LifeAlternative:
    def __init__(self, cube, pop_density=0.1, delay=0):
        self.cube = cube
        self.pop_density = pop_density
        self.delay = delay
        self.live_cells = set()  # Store live cells as (x, y) coordinates
        self.current_grid = cube.instantiate_arr(cube.face_width)
        self.new_grid = cube.instantiate_arr(cube.face_width)
        self.NEIGHBOR_OFFSETS = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),          (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]

    def populate_pixel(self, flatCubeArr, x, y, pop_density):
        color = Colors.random_color()
        if random.random() < pop_density:
            flatCubeArr[x][y] = color
            self.cube.set_pixel(x, y, color)
            self.live_cells.add((x, y))
        else:
            flatCubeArr[x][y] = 0
            self.cube.set_pixel(x, y, 0)

    def count_neighbors(self, x, y, old_grid):
        count = 0
        races = {}
        for dx, dy in self.NEIGHBOR_OFFSETS:
            nx, ny, _ = self.cube.confirm_flat_xy(x + dx, y + dy, None)
            if nx is None:
                continue
            neighbor_val = old_grid[nx][ny]
            if neighbor_val != 0:
                count += 1
                races[neighbor_val] = races.get(neighbor_val, 0) + 1
        return count, races

    def update_generation(self):
        candidates = set()
        next_live_cells = set()

        # Collect live cells and their neighbors as candidates
        for x, y in self.live_cells:
            candidates.add((x, y))
            for dx, dy in self.NEIGHBOR_OFFSETS:
                nx, ny, _ = self.cube.confirm_flat_xy(x + dx, y + dy, None)
                if nx is not None:
                    candidates.add((nx, ny))

        # Process each candidate cell
        for x, y in candidates:
            current_val = self.current_grid[x][y]
            neighbor_count, races = self.count_neighbors(x, y, self.current_grid)

            if current_val == 0 and neighbor_count == 3 and races:
                # Birth: Dead cell with exactly 3 neighbors becomes alive
                new_color = max(races, key=races.get)
                self.new_grid[x][y] = new_color
                self.cube.set_pixel(x, y, new_color)
                next_live_cells.add((x, y))
            elif current_val != 0 and (neighbor_count < 2 or neighbor_count > 3):
                # Death: Live cell with < 2 or > 3 neighbors dies
                self.new_grid[x][y] = 0
                if current_val != 0:
                    self.cube.set_pixel(x, y, 0)  # Update LED if state changes
            else:
                # Survival: Keep the cell's current state
                self.new_grid[x][y] = current_val
                if current_val != 0:
                    next_live_cells.add((x, y))
 
        # Swap grids and live cells
        self.current_grid = self.new_grid
        self.new_grid = self.cube.instantiate_arr(self.cube.face_width)
        self.live_cells = next_live_cells

    def get_name(self):
        return "life alt"

    def animate(self, ble_interrupt):
        self.cube.function_every_pixel(self.populate_pixel, self.current_grid, self.pop_density)
        self.cube.show_pixels()

        while not ble_interrupt.in_waiting:
            self.update_generation()
            self.cube.show_pixels()
            time.sleep(self.delay)
