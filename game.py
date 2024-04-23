
class WumpusWorld:
    def __init__(self):
        self.world = [[0] * 4 for _ in range(4)] 
        self.world[0][0] = 1
        self.cur_row = 0
        self.cur_col = 0

    def reset_world(self):
        self.cur_row = 0
        self.cur_col = 0
        self.world = [[0] * 4 for _ in range(4)] 
        self.world[0][0] = 1
        