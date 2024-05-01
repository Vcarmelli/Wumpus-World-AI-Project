WORLD_SIZE = 4

class WumpusWorld:
    def __init__(self):
        pass

    def check_row_column(self, agent_pos, wumpus_pos, row_col):
        agent_x, agent_y = agent_pos
        for i in range(WORLD_SIZE):
            if row_col == 'C':
                if i == wumpus_pos[0]:
                    print("Checking column:", i)
                    if agent_x == wumpus_pos[0]:
                        print("COLUMN:", i, wumpus_pos[0])
                        return True
            elif row_col == 'R':
                if i == wumpus_pos[1]:
                    print("Checking row:", i)
                    if agent_y == wumpus_pos[1]:
                        print("ROW:", i, wumpus_pos[1])
                        return True
        return False


# Test scenario
if __name__ == "__main__":
    wumpus_world = WumpusWorld()
    agent_position = (2, 3)
    wumpus_position = (0, 3)
    print("Agent position:", agent_position)
    print("Wumpus position:", wumpus_position)
    print("same row:")
    print(wumpus_world.check_row_column(agent_position, wumpus_position, 'R'))
    print("same column:")
    print(wumpus_world.check_row_column(agent_position, wumpus_position, 'C'))
