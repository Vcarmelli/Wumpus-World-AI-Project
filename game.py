import random
from helper import Helper
import sys

WORLD_SIZE = 4
func = Helper()

class WumpusWorld:
    def __init__(self):
        self.path = [[0] * 4 for _ in range(4)] 
        self.path[0][0] = 1
        self.world = [[''] * 4 for _ in range(4)] 
        self.world[0][0] = 'A'
        self.cur_row = 0
        self.cur_col = 0
        self.agent = Agent()

    def reset_world(self):
        self.cur_row = 0
        self.cur_col = 0
        self.path = [[0] * 4 for _ in range(4)] 
        self.path[0][0] = 1
        self.world = [[''] * 4 for _ in range(4)] 
        self.world[0][0] = 'A'


    def random_gold_wumpus_pits(self):
        coordinates = set()  # Use a set to ensure uniqueness
        while len(coordinates) < 5:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if x == 0 and y == 0:
                continue
            coordinates.add((x, y))
        return list(coordinates)
    

    def add_stench_breeze(self):
        w_b = { 'W': 'S', 'P': 'B'}
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                for key, adj in w_b.items():
                    if func.check_char([self.world[x][y]], key):
                        self.world = func.assign_char(x, y+1, adj, self.world)
                        self.world = func.assign_char(x, y-1, adj, self.world)
                        self.world = func.assign_char(x+1, y, adj, self.world)
                        self.world = func.assign_char(x-1, y, adj, self.world)


    def prepare_environment(self):
        self.g_w_p_coords = self.random_gold_wumpus_pits()
        chars = ['G', 'W', 'P', 'P', 'P']

        for i, (row, col) in enumerate(self.g_w_p_coords):
            self.world = func.assign_char(row, col, chars[i], self.world)
        self.add_stench_breeze()

        func.print_world(self.world)


    def locate_agent(self):
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                if func.check_char([self.world[x][y]], 'A'):
                    self.world = func.remove_char(x, y, 'A', self.world)

    def move_agent(self, x, y):
        self.agent.location = (x, y)

        if self.game_over():
            sys.exit()
        else:
            self.agent.reset_sensor()
            self.locate_agent()
            self.world = func.assign_char(x, y, 'A', self.world)
            print('ASSIGN A')
            self.perceive_agent(x, y)


    def perceive_agent(self, x, y):
        cell = self.world[x][y]
        perceived = False
        
        if func.check_char(cell, 'B'):
            self.agent.perceive('Breeze')
            perceived = True
        if func.check_char(cell, 'G'):
            self.agent.perceive('Glitter')
            perceived = True
        if func.check_char(cell, 'S'):
            self.agent.perceive('Stench')
            perceived = True
        if not func.is_valid(x, y):
            self.agent.perceive('Bump')
            perceived = True

        if not perceived:
            self.agent.perceive('No perceive')

        # WUMPUS DIED
        # Perceive scream
        

    def game_over(self):
        #print(self.g_w_p_coords[1:])
        for pos in self.g_w_p_coords[1:]:
            if self.agent.location == pos:
                # print("self.agent.location:", self.agent.location)
                # print("pos:", pos)
                print("GAME OVER")
                return True
        return False


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
        self.inference = [[''] * 4 for _ in range(4)] 
        self.prev_moves = [] 
        self.count_loop = 0


    def perceive(self, percept):
        if percept == "No perceive":
            self.kb.add(self.location, self.sensor)
        elif percept in self.sensor:
            self.sensor[percept] = True 
            
        self.kb.add(self.location, self.sensor)
        self.infer()


    def reset_sensor(self):
        for percept in self.sensor:
            self.sensor[percept] = None


    def get_move(self):
        row, col = self.location[0], self.location[1] 
        adj_cells = func.get_adjacent(row, col)
        
        valid_adj_cells = [(x, y) for x, y in adj_cells if func.is_valid(x, y)]        
        random.shuffle(valid_adj_cells)
        print(valid_adj_cells)
        for x, y in valid_adj_cells:
            safety = self.is_move_safe(x, y)
            if safety == -1:
                continue
            else:
                for i in range(len(self.prev_moves) - 2):
                    if (x, y) == self.prev_moves[i]:
                        print(i)
                        print("Current move is the same as a move made two steps ago.")
                        self.count_loop += 1
                        print("self.count_loop", self.count_loop)
                
                    if self.count_loop == 3:
                        self.prev_moves = []
                        self.count_loop = 0
                        valid_adj_cells.remove((x, y))
                        return random.choice(valid_adj_cells)
                        
                print("Current move:", (x, y))
                print("Previous moves:", self.prev_moves)
                
                self.prev_moves.append((x, y))
                return x, y
            
        return random.choice(valid_adj_cells)

    def is_move_safe(self, x, y):
        #print(self.kb.world_info[x][y])
        if not self.kb.world_info[x][y]:
            print('NO KNOWLEDGE')
            return 0
        elif all(value is None for value in self.kb.world_info[x][y].values()):
            print(f'YES ({x}, {y}) SAFE')
            return 1
        elif any(value is None for value in self.kb.world_info[x][y].values()):
            true_values = [key for key, value in self.kb.world_info[x][y].items() if value is True]
            print(f'THERE IS {true_values} in ({x}, {y})')
            return -1
        
    def infer(self):
        row, col = self.location[0], self.location[1] 
        adjacent_cells = func.get_adjacent(row, col)
        predict = { 'Stench': 'W', 'Breeze': 'P', 'Glitter': 'G'}

        for key, value in self.kb.world_info[row][col].items():
            if value == True:
                for adj_row, adj_col in adjacent_cells:
                    if func.is_valid(adj_row, adj_col):
                        prediction = predict.get(key)
                        if key == "Glitter":
                            self.inference = func.assign_char(row, col, prediction, self.inference)
                        else:
                            self.inference = func.assign_char(adj_row, adj_col, prediction, self.inference)

        func.print_world(self.inference)

            


class Knowledge:
    def __init__(self):
        self.world_info = [[{} for _ in range(4)] for _ in range(4)]

    def add(self, pos, sensors):
        self.world_info[pos[0]][pos[1]] = sensors.copy()
        print('pos:', pos)
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
    


if __name__ == '__main__':
    ww = WumpusWorld()
    ww.prepare_environment()

    while True:
        x, y = ww.agent.get_move()
        #print(f"COORDINATE: ({x}, {y})")
        
        ww.move_agent(x, y)
        #ww.agent.is_move_safe(x, y)
        func.print_world(ww.world)
        input()


        