from itertools import combinations

WORLD_SIZE = 4

def print_grid_with_pattern(grid, pattern):
    print("pattern", pattern)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i, j) in pattern:
                print(f'[{cell}]', end=' ')
            else:
                print(f' {cell} ', end=' ')
        print()

def print_patterns_with_grid(grid, patterns):
    print("Grid with Patterns:")
    for idx, pattern in enumerate(patterns, 1):
        print(f"Pattern {idx}:")
        print_grid_with_pattern(grid, pattern)
        print()

def get_adjacent(x, y):
    adjacent_coords = [
        (x, y + 1),  # Right
        (x, y - 1),  # Left
        (x + 1, y),  # Down
        (x - 1, y)   # Up
    ]
    
    # Filter out coordinates outside the grid
    adjacent_coords = [(x, y) for (x, y) in adjacent_coords if 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE]
    
    return list(combinations(adjacent_coords, 3))

grid = [
    ['S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S']
]

patterns_for_grid = []

# Generate patterns for each cell in the grid
for i in range(WORLD_SIZE):
    for j in range(WORLD_SIZE):
        patterns_for_cell = get_adjacent(i, j)
        patterns_for_grid.append(patterns_for_cell)

# Print the grid with its corresponding patterns
print_patterns_with_grid(grid, patterns_for_grid)
