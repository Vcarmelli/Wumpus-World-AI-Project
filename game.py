import random

WORLD_SIZE = 4

class WumpusWorld:
    def __init__(self):
        self.world = [[''] * 4 for _ in range(4)] 
        self.world[0][0] = 1
        self.cur_row = 0
        self.cur_col = 0

    def reset_world(self):
        self.cur_row = 0
        self.cur_col = 0
        self.world = [[''] * 4 for _ in range(4)] 
        self.world[0][0] = 1

    def random_gold_wumpus_pits(self):
        coordinates = set()  # Use a set to ensure uniqueness
        while len(coordinates) < 5:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            coordinates.add((x, y))
        return list(coordinates)
    
    def assign_environment(self, x, y, character):
        if 0 <= x < 4 and 0 <= y < 4:
            current_char = self.world[x][y]
            if current_char != 0:
                self.world[x][y] = str(current_char) + character
            else:
                self.world[x][y] = character
        else:
            print("Error: Coordinates out of bounds!")
            pass

    def check_char(self, cell, letter):
        for string in cell:
            for char in str(string):
                if char == letter:
                    return True
            #     print("let", let)
            # print("char", char)
        return False

    def add_stench_breeze(self):
        w_b = { 'W': 'S', 'P': 'B'}
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                for key, adj in w_b.items():
                    if self.check_char([self.world[x][y]], key):
                        self.assign_environment(x, y+1, adj)
                        self.assign_environment(x, y-1, adj)
                        self.assign_environment(x+1, y, adj)
                        self.assign_environment(x-1, y, adj)

    def prepare_environment(self):
        g_w_p_coords = self.random_gold_wumpus_pits()
        chars = ['G', 'W', 'P', 'P', 'P']

        for i, (row, col) in enumerate(g_w_p_coords):
            self.assign_environment(row, col, chars[i])
        self.add_stench_breeze()

        self.print_world(self.world)

        
    def print_world(self, array):    
        print("+" + "-" * 23 + "+")
        for i in range(4):
            print("|  ", end="")
            for j in range(4):
                print(array[i][j], end="  ")
                print("|  ", end="")
            print()
            print("+" + "-" * 23 + "+")

        


# if __name__ == '__main__':
#     ww = WumpusWorld()
#     ww.prepare_environment()

        