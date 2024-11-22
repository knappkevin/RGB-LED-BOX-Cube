import random, time

'''
variation of the life animation that is optimized for speed but suffers on memory
'''
class FastLife:
    def __init__(self, cube, pop_density, delay):
        self.cube = cube
        self.pop_density = pop_density
        self.delay = delay
        self.live_cells = set()  # Store live cells as (x, y) coordinates
        self.NEIGHBOR_OFFSETS = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),          (1, 0),
            (-1, -1), (0, -1), (1, -1)]


    def populate_pixel(self, flatCubeArr, x, y, pop_density):
        color = self.cube.random_color()
        if random.random() < pop_density:
            flatCubeArr[x][y] = color
            self.live_cells.add((x, y))
        else:
            flatCubeArr[x][y] = 0


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
        candidates = set()  # Use a set to avoid duplicates
        new_grid = self.cube.instantiate_arr(self.cube.face_width)
        next_live_cells = set()  # Local variable for the next generation's live cells
        
        # Collect live cells and their neighbors as candidates
        for x, y in self.live_cells:
            candidates.add((x, y))
            for dx, dy in self.NEIGHBOR_OFFSETS:
                nx, ny, _ = self.cube.confirm_flat_xy(x + dx, y + dy, None)
                if nx is not None:
                    candidates.add((nx, ny))
            self.live_cells.discard((x, y))
        
        # Process each candidate cell
        for x, y in candidates:
            current_val = self.cube.flat_cube_arr[x][y]  # Use current color (live state) from the cube
            neighbor_count, races = self.count_neighbors(x, y, self.cube.flat_cube_arr)
            
            # Determine cell's next state based on neighbor count
            if current_val == 0 and neighbor_count == 3:
                # Birth: Dead cell with exactly 3 neighbors becomes alive with the most common race color
                new_grid[x][y] = max(races, key=races.get)
                next_live_cells.add((x, y))
            elif current_val != 0 and (neighbor_count < 2 or neighbor_count > 3):
                # Death: Live cell with < 2 or > 3 neighbors dies
                new_grid[x][y] = 0
            else:
                # Survival: Keep the cell's current state
                new_grid[x][y] = current_val
                if current_val != 0:
                    next_live_cells.add((x, y))
        
        # Update the cube and refresh live cells
        self.cube.flat_cube_arr = new_grid

        # Swap live cells for the next generation
        self.live_cells = next_live_cells

    def get_name(self):
        return "fast life"

    def animate(self, ble_intrrupt):
        self.cube.function_every_pixel(self.populate_pixel, self.cube.flat_cube_arr, self.pop_density)
        self.cube.set_pixels()
        self.cube.show_pixels()

        while not ble_intrrupt.in_waiting:
            self.update_generation()
            self.cube.set_pixels()
            self.cube.show_pixels()
            time.sleep(self.delay)
