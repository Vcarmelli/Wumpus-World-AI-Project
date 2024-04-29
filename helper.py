WORLD_SIZE = 4

class Helper:
    def is_valid(self, x, y):
        return 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE
    
    def get_adjacent(self, x, y):
        return [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

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
                horizontal_triangle1 = [(i, j), (i + 1, j + 1), (i, j + 2)]
                horizontal_triangle2 = [(i + 1, j), (i, j + 1), (i + 1, j + 2)]
                # Check if all coordinates are within bounds before adding to patterns_list
                if all(0 <= coord[0] < WORLD_SIZE and 0 <= coord[1] < WORLD_SIZE for triangle in [horizontal_triangle1, horizontal_triangle2] for coord in triangle):
                    patterns_list.extend([{"pattern": horizontal_triangle1, "location": (i, j + 1)}, {"pattern": horizontal_triangle2, "location": (i + 1, j + 1)}])

                # Generate vertical patterns
                vertical_triangle1 = [(i, j), (i + 1, j + 1), (i + 2, j)]
                vertical_triangle2 = [(i, j + 1), (i + 1, j), (i + 2, j + 1)]
                # Check if all coordinates are within bounds before adding to patterns_list
                if all(0 <= coord[0] < WORLD_SIZE and 0 <= coord[1] < WORLD_SIZE for triangle in [vertical_triangle1, vertical_triangle2] for coord in triangle):
                    patterns_list.extend([{"pattern": vertical_triangle1, "location": (i + 1, j)}, {"pattern": vertical_triangle2, "location": (i + 1, j + 1)}])


        print("patterns_list:", patterns_list)
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




h = Helper()

# def print_grid_with_pattern(grid, pattern):
#     for i, row in enumerate(grid):
#         for j, cell in enumerate(row):
#             if (i, j) in pattern:
#                 print(f'[{cell}]', end=' ')
#             else:
#                 print(cell, end=' ')
#         print()

# def print_patterns_with_grid(grid, patterns):
#     print("Grid with Patterns:")
#     for idx, pattern in enumerate(patterns, 1):
#         print(f"Pattern {idx}:")
#         print_grid_with_pattern(grid, pattern)
#         print()

# # Example 4x4 grid
# grid = [
#     ['S', 'S', 'S', 'S'],
#     ['S', 'S', 'S', 'S'],
#     ['S', 'S', 'S', 'S'],
#     ['S', 'S', 'S', 'S']
# ]

# # Generate patterns dynamically for a 4x4 grid
h.generate_patterns()

# # Print each grid with its pattern
# print_patterns_with_grid(grid, patterns)


