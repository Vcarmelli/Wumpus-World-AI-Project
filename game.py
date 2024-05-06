import random
from helper import Helper
import sys

WORLD_SIZE = 4
func = Helper()

class WumpusWorld:
    def __init__(self):
        self.agent = Agent()
        self.cur_row = 0
        self.cur_col = 0
        self.path = [[0] * 4 for _ in range(4)] 
        self.path[0][0] = 1
        self.world = [[''] * 4 for _ in range(4)] 
        self.world[0][0] = 'A'

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
            elif x == 0 and y == 1:
                continue
            elif x == 1 and y == 0:
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
        self.perceive_agent(self.cur_row, self.cur_col)


    def locate_agent(self):
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                if func.check_char([self.world[x][y]], 'A'):
                    self.world = func.remove_char(x, y, 'A', self.world)

    def move_agent(self, x, y):
        self.agent.location = (x, y)
        self.agent.reset_sensor()

        self.perceive_agent(x, y)
        self.agent.clear_safe()   
        print("AGENT INFERENCE")  
        func.print_world(self.agent.kb.inference)
        self.locate_agent()
        self.world = func.assign_char(x, y, 'A', self.world)
        self.agent.score -= 1
        print("WORLD", self.world)
        func.print_world(self.world)


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
        if func.is_boundary_cell(x, y):
            self.agent.perceive('Bump')
            perceived = True
        

        if not perceived:
            self.agent.perceive('No perceive')

        # WUMPUS DIED
        # Perceive scream


        

    def game_status(self):
        for i, pos in enumerate(self.g_w_p_coords):
            if self.agent.location == pos: # if the agent is in eiher gold, wumpus, or pits locations
                return i
        else:
            if self.agent.has_gold:
                return 9
            elif self.agent.w_found and not self.agent.w_killed:
                return 10
            
        return -1
        
    def is_wumpus_killed(self, direction):
        wumpus_xy = self.g_w_p_coords[1]

        if direction == 'N' or direction == 'S':
            if func.check_row_column(self.agent.location, wumpus_xy, 'C'):
                self.world = func.remove_char(wumpus_xy[0], wumpus_xy[1], 'W', self.world[:])
                print("KILLED ", wumpus_xy)
                self.agent.w_killed = True
                self.agent.perceive_scream(self.agent.location, 'C')
                return True
        elif direction == 'E' or direction == 'W':
            if func.check_row_column(self.agent.location, wumpus_xy, 'R'):
                self.world = func.remove_char(wumpus_xy[0], wumpus_xy[1], 'W', self.world[:])
                print("KILLED ", wumpus_xy)
                self.agent.w_killed = True
                self.agent.perceive_scream(self.agent.location, 'C')
                return True

        print("NOT KILLED wumpus_xy", wumpus_xy)
        print("direction", self.agent.facing)
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
        self.facing = 'S'
        self.has_gold = False
        self.score = 1000
        self.kb = Knowledge()
        self.count_loop = 0
        self.prev_moves = [] 
        self.unsafe = []
        self.w_pos = ()
        self.w_found = False
        self.w_killed = False
        


    def perceive(self, percept):
        if percept == "No perceive":
            self.kb.add(self.location, self.sensor)
        elif percept in self.sensor:
            self.sensor[percept] = True 
            
        self.kb.add(self.location, self.sensor)
        self.infer()

    def perceive_scream(self, xy, row_col):
        percept = "Scream"
        if row_col == 'C': 
            for j in range(WORLD_SIZE):
                if percept in self.sensor:
                    self.sensor[percept] = True 
                    self.kb.add((xy[0], j), self.sensor)
                print(self.kb.world_info[xy[0]][j]['Scream'])
        elif row_col == 'R':  
            for i in range(WORLD_SIZE):
                if percept in self.sensor:
                    self.sensor[percept] = True 
                    self.kb.add((i, xy[1]), self.sensor)
                print(self.kb.world_info[[i]][xy[1]]['Scream'])

        self.kb.print_world_info()
    

    def reset_sensor(self):
        for percept in self.sensor:
            self.sensor[percept] = None

    def get_move(self, got_gold):
        if got_gold:
            return self.back_to_init_move()
        else:
            return self.normal_move()

    def normal_move(self):
        row, col = self.location
        adj_cells = func.get_adjacent(row, col)
        
        valid_adj_cells = [(x, y) for x, y in adj_cells if func.is_valid(x, y)]        
        random.shuffle(valid_adj_cells)
        
        for x, y in valid_adj_cells:
            safety = self.is_move_safe(x, y)
            if safety == -1:
                continue
            elif safety == 0 and self.predict_unsafe(x, y):   # agent doesn't have knowledge about that cell  
                continue                                      # then it will check the move based on the prediction made from the hints
            
            for i in range(len(self.prev_moves) - 2):
                if (x, y) == self.prev_moves[i]: # check the move two steps before if same
                    self.count_loop += 1
            
                if self.count_loop == 2:           # if it got stuck two times
                    self.prev_moves = []           # just get a random step except that move that cause the loop
                    self.count_loop = 0
                    valid_adj_cells.remove((x, y))
                    return random.choice(valid_adj_cells)
                    
            self.prev_moves.append((x, y))
            return x, y
            
        return random.choice(valid_adj_cells)

    def is_move_safe(self, x, y):
        if not self.kb.world_info[x][y]:    # no knowledge 
            return 0
        elif all(value is None for value in self.kb.world_info[x][y].values()):
            print(f'({x}, {y}) is safe')   # cell is safe base on the knwoledge from the senses
            return 1
        elif any(value is None for value in self.kb.world_info[x][y].values()):
            true_values = [key for key, value in self.kb.world_info[x][y].items() if value is True]
            print(f'There is a {true_values} in ({x}, {y})')
            return -1
        
    def back_to_init_move(self):
        row, col = self.location
        adj_cells = func.get_adjacent(row, col)
        
        valid_adj_cells = [(x, y) for x, y in adj_cells if func.is_valid(x, y)]        
        valid_adj_cells.sort(key=lambda cell: abs(cell[0] - 0) + abs(cell[1] - 0))

        for x, y in valid_adj_cells:
            safety = self.is_move_safe(x, y)
            
            if safety == 0 and self.predict_unsafe(x, y):        
                continue                             
            for i in range(len(self.prev_moves) - 2):
                if (x, y) == self.prev_moves[i]:
                    self.count_loop += 1
                if self.count_loop == 2:
                    self.prev_moves = []
                    self.count_loop = 0
                    valid_adj_cells.remove((x, y))
                    return random.choice(valid_adj_cells)
            
            self.prev_moves.append((x, y))
            return x, y
        
        return random.choice(valid_adj_cells)
        
        
    def direction(self, x, y):
        row, col = self.location
        if x == row - 1:
            self.facing = 'N'
        elif x == row + 1:
            self.facing = 'S'
        elif y == col - 1:
            self.facing = 'W'
        elif y == col + 1:
            self.facing = 'E'


    def grab(self, x, y, world):
        world = func.remove_char(x, y, 'G', world[:])
        self.score += 1000
        self.has_gold = True
        return world

    def infer(self):
        predict = { 'Stench': 'W', 'Breeze': 'P', 'Glitter': 'G'}

        checked_stench = True
        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):
                for key, value in self.kb.world_info[i][j].items():
                    prediction = predict.get(key)
                    if prediction and value:
                            if key == "Glitter":
                                self.kb.inference = func.assign_char(i, j, prediction, self.kb.inference)
                            for pattern in self.kb.possible_pos:
                                if all(self.kb.world_info[coord[0]][coord[1]].get(key) for coord in pattern["pattern"]):
                                    row, col = pattern["location"]
                                    print("infer kb: ", self.kb.inference)
                                    self.kb.inference = func.assign_char(row, col, prediction, self.kb.inference)
                                    if key == "Stench" and not self.w_found:
                                        if self.check_stench_pattern(pattern): 
                                            checked_stench = False
                                        if checked_stench:        
                                            self.wumpus_located(row, col, True)
                                            self.direction(1, 1) if pattern["location"] == (0, 0) else self.direction(row, col) 
                                            print("FACE AFTER STENCH: ", self.facing)
                                            print("pattern['location']", pattern["location"])
                                            self.kb.possible_pos.remove(pattern)
                                            print("Pattern removed:", pattern)
                                            checked_stench = False


    def check_stench_pattern(self, pattern):
        if len(pattern["pattern"]) == 3:
            print("CHECK 3 PATTERNS")
            if all(self.kb.world_info[coord[0]][coord[1]].get("Stench") for coord in pattern["pattern"]):                
                row, col = pattern["location"]
                self.wumpus_located(row, col, True)
                self.direction(row, col)
                print("FACE AFTER 3 PATTS: ", self.facing)
                print(row, col)
            return True
        print("NOCHECK 3")
        return False

    def clear_safe(self):
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                if self.kb.world_info[x][y]:
                    if all(value is None for value in self.kb.world_info[x][y].values()):
                        self.kb.inference[x][y] = ''
                elif self.kb.inference[x][y] != '':
                    if (x, y) not in self.unsafe: self.unsafe.append((x, y))  # reconrd unsafe cells based on prediction
                    

    def predict_unsafe(self, x, y):
        if (x, y) in self.unsafe:
            print("Unsafe Cells:", self.unsafe) # base on patterns of hints
            print((x, y))
            return True
        return False

    def wumpus_located(self, x, y, found):
        self.w_pos = (x, y)
        self.w_found = found


class Knowledge:
    def __init__(self):
        self.possible_pos = func.generate_patterns()
        self.world_info = [[{} for _ in range(4)] for _ in range(4)]
        self.inference = [[''] * 4 for _ in range(4)] 


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
    


        