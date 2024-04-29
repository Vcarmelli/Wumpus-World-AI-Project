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
        patterns = []
        for i in range(-1, WORLD_SIZE):
            for j in range(-1, WORLD_SIZE):
                # Generate horizontal patterns
                patterns.append([(i, j), (i + 1, j + 1), (i, j + 2)])
                patterns.append([(i + 1, j), (i, j + 1), (i + 1, j + 2)])
                # Generate vertical patterns
                patterns.append([(i, j), (i + 1, j + 1), (i + 2, j)])
                patterns.append([(i, j + 1), (i + 1, j), (i + 2, j + 1)])
        patterns = [pattern for pattern in patterns if sum(1 for coord in pattern if 0 <= coord[0] < WORLD_SIZE and 0 <= coord[1] < WORLD_SIZE) > 1]
        print("patterns:", patterns)
        return patterns
    
    def print_world(self, world):    
        print("+" + "-" * 23 + "+")
        for i in range(4):
            print("|  ", end="")
            for j in range(4):
                print(world[i][j], end="  ")
                print("|  ", end="")
            print()
            print("+" + "-" * 23 + "+")

# h = Helper()


def print_grid_with_pattern(grid, pattern):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i, j) in pattern:
                print(f'[{cell}]', end=' ')
            else:
                print(cell, end=' ')
        print()

def print_patterns_with_grid(grid, patterns):
    print("Grid with Patterns:")
    for idx, pattern in enumerate(patterns, 1):
        print(f"Pattern {idx}:")
        print_grid_with_pattern(grid, pattern)
        print()

# Example 4x4 grid
grid = [
    ['S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S']
]

# # Generate patterns dynamically for a 4x4 grid
# patterns = h.generate_patterns()

# # Print each grid with its pattern
# print_patterns_with_grid(grid, patterns)


from itertools import combinations

def get_adjacent(x, y):
    adjacent_coords = [
        (x, y + 1),  # Right
        (x, y - 1),  # Left
        (x + 1, y),  # Down
        (x - 1, y)   # Up
    ]
    
    # Filter out coordinates outside the grid
    adjacent_coords = [(x, y) for (x, y) in adjacent_coords if 0 <= x < 4 and 0 <= y < 4]
    
    return list(combinations(adjacent_coords, 3))


for i in range(WORLD_SIZE):
    for j in range(WORLD_SIZE):
        patts = []
        patts.append(get_adjacent(i, j))

        print_patterns_with_grid(grid, patts)
