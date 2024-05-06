WORLD_SIZE = 4

class Helper:
    def is_valid(self, x, y):
        return 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE
    
    def check_row_column(self, agent_pos, wumpus_pos, row_col):
        agent_x, agent_y = agent_pos
        for i in range(WORLD_SIZE):
            if row_col == 'C':
                if i == wumpus_pos[1]:
                    if agent_y == wumpus_pos[1]:
                        print("Wumpus killed in COLUMN:", i)
                        return True
            elif row_col == 'R':
                if i == wumpus_pos[0]:
                    if agent_x == wumpus_pos[0]:
                        print("Wumpus killed in ROW:", i)
                        return True
        return False
    
    def get_adjacent(self, x, y):
        return [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
    
    def is_boundary_cell(self, x, y):
        return (x == 0 or x == 3 or y == 0 or y == 3)

    def assign_char(self, x, y, character, grid):
        if self.is_valid(x, y):
            current_chars = set(grid[x][y])
            current_chars.add(character)
            grid[x][y] = ''.join(sorted(current_chars))
        else:
            #print("Error: Coordinates out of bounds!")
            pass
        return grid

    def remove_char(self, x, y, character, grid):
        if self.is_valid(x, y):
            current_chars = set(grid[x][y])
            if character in current_chars:
                current_chars.remove(character)
                grid[x][y] = ''.join(sorted(current_chars))
        else:
            pass
        return grid      

    def check_char(self, cell, letter):
        return any(letter in string for string in cell)
    

    def generate_patterns(self):
        patterns_list = []
        patterns = {
            "pattern": [],
            "location": ()
        }
        for i in range(-1, WORLD_SIZE):
            for j in range(-1, WORLD_SIZE):
                # Generate horizontal patterns
                triangle = [(i, j), (i + 1, j + 1), (i, j + 2)]
                patterns_list.append({"pattern": triangle, "location": (i, j + 1)})

                triangle = [(i + 1, j), (i, j + 1), (i + 1, j + 2)]
                patterns_list.append({"pattern": triangle, "location": (i + 1, j + 1)})

                # Generate vertical patterns
                triangle = [(i, j), (i + 1, j + 1), (i + 2, j)]
                patterns_list.append({"pattern": triangle, "location": (i + 1, j)})

                triangle = [(i, j + 1), (i + 1, j), (i + 2, j + 1)]
                patterns_list.append({"pattern": triangle, "location": (i + 1, j + 1)})

        # ensure there are at least two valid cell patterns in the grid
        patterns_list = [pattern for pattern in patterns_list if sum(1 for coord in pattern["pattern"] if self.is_valid(coord[0], coord[1])) > 1] 

        # remove the cells outside the world size
        for pattern in patterns_list:
            pattern["pattern"] = [coord for coord in pattern["pattern"] if self.is_valid(coord[0], coord[1])]

        return patterns_list
    
    def print_world(self, world):    
        print("+" + "-" * 23 + "+")
        for i in range(4):
            print("|  ", end="")
            for j in range(4):
                print(world[i][j], end="  ")
                print("|  ", end="")
            print()
            print("+" + "-" * 23 + "+")
