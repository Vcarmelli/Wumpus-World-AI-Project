import random

WORLD_SIZE = 4

class WumpusWorld:
    def __init__(self):
        self.path = [[0] * 4 for _ in range(4)] 
        self.world = [[''] * 4 for _ in range(4)] 
        self.world[0][0] = 'A'
        self.cur_row = 0
        self.cur_col = 0
        self.agent = Agent()

    def reset_world(self):
        self.cur_row = 0
        self.cur_col = 0
        self.path = [[0] * 4 for _ in range(4)] 
        self.world = [[''] * 4 for _ in range(4)] 
        self.world[0][0] = 'A'

    def print_world(self):    
        print("+" + "-" * 23 + "+")
        for i in range(4):
            print("|  ", end="")
            for j in range(4):
                print(self.world[i][j], end="  ")
                print("|  ", end="")
            print()
            print("+" + "-" * 23 + "+")

    def random_gold_wumpus_pits(self):
        coordinates = set()  # Use a set to ensure uniqueness
        while len(coordinates) < 5:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if x == 0 and y == 0:
                continue
            coordinates.add((x, y))
        return list(coordinates)
    
    def is_valid(self, x, y):
        return 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE
    
    def assign_environment(self, x, y, character):
        if self.is_valid(x, y):
            current_chars = set(self.world[x][y])
            current_chars.add(character)
            self.world[x][y] = ''.join(sorted(current_chars))
        else:
            #print("Error: Coordinates out of bounds!")
            pass

    def remove_char(self, x, y, character):
        if self.is_valid(x, y):
            current_chars = set(self.world[x][y])
            if character in current_chars:
                current_chars.remove(character)
                self.world[x][y] = ''.join(sorted(current_chars))
        else:
            # Handle coordinates out of bounds
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

        self.print_world()


    def locate_agent(self):
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                if self.check_char([self.world[x][y]], 'A'):
                    self.remove_char(x, y, 'A')

    def move_agent(self, x, y):
        self.locate_agent()
        self.assign_environment(x, y, 'A')
        self.agent.location = (x, y)
        self.perceive_agent(x, y)
        return

    def perceive_agent(self, x, y):
        if self.check_char(self.world[x][y], 'S'):
            self.agent.perceive('Stench')
        if self.check_char(self.world[x][y], 'B'):
            self.agent.perceive('Breeze')
        if self.check_char(self.world[x][y], 'G'):
            self.agent.perceive('Glitter')
        if not self.is_valid(x, y):
            self.agent.perceive('Bump')

        # WUMPUS DIED
        # Perceive scream


class Agent:
    def __init__(self):
        self.sensor = {
            'Stench': None,
            'Breeze': None,
            'Glitter': None,
            'Bump': None,
            'Scream': None
        }
        self.location = (0, 0)
        self.score = 1000
        self.kb = Knowledge()


    def perceive(self, percept):
        if percept in self.sensor:
            self.sensor[percept] = True 

        print(self.location)
        self.kb.add(self.location, self.sensor)

        for sensor_type in self.sensor:
            self.sensor[sensor_type] = None

    


class Knowledge:
    def __init__(self):
        self.world_info = [[{}] * 4 for _ in range(4)] 

    def add(self, pos, sensors):
        self.world_info[pos[0]][pos[1]] = sensors
        print('pos', pos)
        self.print_world_info()


    def print_world_info(self):
        for i in range(4):
            print("+" + "-" * 35 + "+" + "-" * 35 + "+"+ "-" * 35 + "+"+ "-" * 35 + "+")
            for j in range(4):
                sensors = self.world_info[i][j]
                print("|", end="")
                if sensors:
                    for sensor_type, value in sensors.items():
                        if isinstance(value, bool):
                            value_str = str(value)[:2]  # Get first 2 letters
                        elif value is None:
                            value_str = "None"[:2]  # Get first 2 letters
                        print(f" {sensor_type[0]}: {value_str} ", end="")
                else:
                    print(" " * 35, end="")
            print("|")
        print("+" + "-" * 35 + "+" + "-" * 35 + "+"+ "-" * 35 + "+"+ "-" * 35 + "+")
    


# if __name__ == '__main__':
#     ww = WumpusWorld()
#     ww.prepare_environment()

#     while True:
#         coordinate = input("COORDINATE: ")
#         x, y = int(coordinate[0]), int(coordinate[1])

#         if ww.is_valid(x, y):
#             ww.move_agent(x, y)
#             ww.print_world()
            
#         else:
#             print("Invalid coordinates. Please enter valid coordinates.")


        