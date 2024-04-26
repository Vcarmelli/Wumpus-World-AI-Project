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
    
    def print_world(self, world):    
        print("+" + "-" * 23 + "+")
        for i in range(4):
            print("|  ", end="")
            for j in range(4):
                print(world[i][j], end="  ")
                print("|  ", end="")
            print()
            print("+" + "-" * 23 + "+")