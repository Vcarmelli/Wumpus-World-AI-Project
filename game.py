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
        print("AFTER CLEARING")      
        func.print_world(self.agent.kb.inference)
        self.locate_agent()
        self.world = func.assign_char(x, y, 'A', self.world)
        self.agent.score -= 1


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
        

    def game_status(self):
        for i, pos in enumerate(self.g_w_p_coords):
            if self.agent.location == pos:
                # print("self.agent.location:", self.agent.location)
                # print("pos:", pos)
                #print("GAME OVER")
                return i
        else:
            if self.agent.has_gold:
                return 9
            elif self.agent.w_found:
                return 10
            
        return -1
        
    def is_wumpus_killed(self, direction):
        wumpus_x, wumpus_y = self.g_w_p_coords[1]
        if direction == 'N' or direction == 'S':
            for col in range(WORLD_SIZE):
                if col == wumpus_y:
                    print("wumpus_y", wumpus_y)
                    self.world = func.remove_char(wumpus_x, col, 'W', self.world[:])
                    return True
        elif direction == 'E' or direction == 'W':
            for row in range(WORLD_SIZE):
                if row == wumpus_x:
                    print("wumpus_x", wumpus_x)
                    self.world = func.remove_char(row, wumpus_y, 'W', self.world[:])
                    return True
        else:
            print("NOT KILLED wumpus_xy", wumpus_x, wumpus_y)
            print("direction", direction)
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


    def perceive(self, percept):
        if percept == "No perceive":
            self.kb.add(self.location, self.sensor)
        elif percept in self.sensor:
            self.sensor[percept] = True 
            
        self.kb.add(self.location, self.sensor)
        #self.infer()
        self.predict()
    

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
        #print(valid_adj_cells)
        
        for x, y in valid_adj_cells:
            safety = self.is_move_safe(x, y)
            if safety == -1:
                continue
            elif safety == 0 and self.predict_unsafe(x, y):   # agent doesn't have knowledge about that cell  
                print('NO KNOWLEDGE and unsafe')                 # then it will check the move based on the prediction made from the hints
                continue                                            
            
            for i in range(len(self.prev_moves) - 2):
                if (x, y) == self.prev_moves[i]:
                    # print("Current move is the same as a move made two steps ago.")
                    self.count_loop += 1
                    #print("self.count_loop", self.count_loop)
            
                if self.count_loop == 3:
                    self.prev_moves = []
                    self.count_loop = 0
                    valid_adj_cells.remove((x, y))
                    return random.choice(valid_adj_cells)
                    
            # print("Current move:", (x, y))
            # print("Previous moves:", self.prev_moves)
            
            self.prev_moves.append((x, y))
            return x, y
            
        return random.choice(valid_adj_cells)

    def is_move_safe(self, x, y):
        #print(self.kb.world_info[x][y])
        if not self.kb.world_info[x][y]: # no knowledge 
            return 0
        elif all(value is None for value in self.kb.world_info[x][y].values()):
            print(f'YES ({x}, {y}) SAFE')
            return 1
        elif any(value is None for value in self.kb.world_info[x][y].values()):
            true_values = [key for key, value in self.kb.world_info[x][y].items() if value is True]
            print(f'THERE IS {true_values} in ({x}, {y})')
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
                if self.count_loop == 3:
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

        
    def infer(self):
        row, col = self.location
        adjacent_cells = func.get_adjacent(row, col)
        predict = { 'Stench': 'W', 'Breeze': 'P', 'Glitter': 'G'}

        for key, value in self.kb.world_info[row][col].items():
            if value == True:
                for adj_row, adj_col in adjacent_cells:
                    if func.is_valid(adj_row, adj_col):
                        prediction = predict.get(key)
                        if key == "Glitter":
                            self.kb.inference = func.assign_char(row, col, prediction, self.kb.inference)
                        else:
                            self.kb.inference = func.assign_char(adj_row, adj_col, prediction, self.kb.inference)

        func.print_world(self.kb.inference)
        self.predict()
        print('AFTER INFER THEN PREDICT')
        func.print_world(self.kb.inference)

    def grab(self, x, y, world):
        world = func.remove_char(x, y, 'G', world[:])
        self.score += 1000
        self.has_gold = True
        return world

    def predict(self):
        possible_pos = func.generate_patterns()
        predict = { 'Stench': 'W', 'Breeze': 'P', 'Glitter': 'G'}
        # CAN BE USE FOR CHECKING 
        # BETTER IF 3 MATCH THE POSSIBLE POS
        # CONSIDER THE NUMBER OF PITS AND WUMPUS 
        checked_stench = False
        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):
                for key, value in self.kb.world_info[i][j].items():
                    if value:
                        prediction = predict.get(key)
                        if key == "Glitter":
                            self.kb.inference = func.assign_char(i, j, prediction, self.kb.inference)
                        for pattern in possible_pos:
                            if all(self.kb.world_info[coord[0]][coord[1]].get(key) for coord in pattern["pattern"]):
                                row, col = pattern["location"]
                                #print("Pattern:", pattern["pattern"], "Location:", pattern["location"])
                                self.kb.inference = func.assign_char(row, col, prediction, self.kb.inference)
                                if key == "Stench":
                                    if checked_stench:
                                        self.check_stench_pattern(pattern)  
                                    else:        
                                        self.wumpus_located(row, col, True)
                                        self.direction(1, 1) if pattern["location"] == (0, 0) else self.direction(row, col) 
                                        print("FACE AFTER STENCH: ", self.facing)
                                        print(row, col)
                                        checked_stench = True
                            
        print(self.kb.inference)
        #self.clear_safe()                                
        #func.print_world(self.kb.inference) 

    def check_stench_pattern(self, pattern):
        if len(pattern["pattern"]) == 3:
            print("CHECK 3 PATTERNS")
            if all(self.kb.world_info[coord[0]][coord[1]].get("Stench") for coord in pattern["pattern"]):                
                row, col = pattern["location"]
                self.wumpus_located(row, col, True)
                self.direction(row, col)
                print("FACE AFTER 3 PATTS: ", self.facing)
                print(row, col)
            #return True
        print("NOCHECK 3")
        #return False

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
            print("UNSAFE:", self.unsafe)
            print((x, y))
            return True
        return False

    def wumpus_located(self, x, y, found):
        self.w_pos = (x, y)
        self.w_found = found


class Knowledge:
    def __init__(self):
        self.world_info = [[{} for _ in range(4)] for _ in range(4)]
        self.inference = [[''] * 4 for _ in range(4)] 


    def add(self, pos, sensors):
        self.world_info[pos[0]][pos[1]] = sensors.copy()
        print('pos:', pos)
        #self.print_world_info()


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
#         x, y = ww.agent.get_move()
#         #print(f"COORDINATE: ({x}, {y})")
        
#         ww.move_agent(x, y)
#         #ww.agent.is_move_safe(x, y)
#         func.print_world(ww.world)
#         input()


        