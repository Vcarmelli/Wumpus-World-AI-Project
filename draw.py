import pygame as pg

space = 90
mg_x = 70
mg_y = 150
WORLD_SIZE = 4

AQUA = (49, 255, 255)
WHITE = (255, 255, 255)
GREEN = (67, 83, 24)
LIGHT_GREEN = (194, 203, 159)
BLUE = (6, 61, 81)

pg.font.init()

class Draw:
    def __init__(self, screen):
        self.screen = screen
        self.agent_img = pg.image.load("assets/agent.png")
        self.agent_side_img = pg.image.load("assets/agent_side.png")
        self.agent_victory_img = pg.image.load("assets/agent_victory.png")
        self.arrow_img = pg.image.load("assets/arrow.png")
        self.arrow_side_img = pg.image.load("assets/arrow_side.png")
        self.breeze_img = pg.image.load("assets/cell_breeze.png")
        self.breeze_stench_img = pg.image.load("assets/cell_breeze-stench.png")
        self.gold_img = pg.image.load("assets/cell_gold.png")
        self.pit_img = pg.image.load("assets/cell_pit.png")
        self.stench_img = pg.image.load("assets/cell_stench.png")
        self.wumpus_img = pg.image.load("assets/cell_wumpus.png")

        self.font = pg.font.SysFont('Arial Black', 20)

    def board(self):
        pg.draw.rect(self.screen, LIGHT_GREEN, pg.Rect(mg_x, mg_y, 360, 360), 7)

        i = 1
        while (i * space) < 360:
            line_width = 3 
            pg.draw.line(self.screen, LIGHT_GREEN, (mg_x, mg_y + i * space), (mg_x + 355, mg_y + i * space), line_width)
            pg.draw.line(self.screen, LIGHT_GREEN, (mg_x + i * space, mg_y), (mg_x + i * space, mg_y + 355), line_width)
            i += 1

    def agent(self, row, col, direction):
        x = mg_x + col * space +10
        y = mg_y + row * space +20

        if direction == 'N':
            y -= 10
            self.screen.blit(self.agent_img, (x, y))
        elif direction == 'S':
            self.screen.blit(self.agent_img, (x, y))
        elif direction == 'W':
            self.screen.blit(self.agent_side_img, (x, y))
        elif direction == 'E':
            agent_rightside = pg.transform.flip(self.agent_side_img, True, False)
            self.screen.blit(agent_rightside, (x, y))
        elif direction == 'V':
            self.screen.blit(self.agent_victory_img, (x-10, y-20))
        
        self.board()

    def environment(self, world):
        for row in range(WORLD_SIZE):
            for col in range(WORLD_SIZE):
                self.fill_env(row, col, world)
                

    def fill_env(self, row, col, world):
        cell_type = world[row][col]

        x = mg_x + col * space
        y = mg_y + row * space

        if len(cell_type) > 1 and cell_type[0] == 'A':
            if len(cell_type) == 3 and cell_type[1] == 'B' and cell_type[2] == 'S':
                self.screen.blit(self.breeze_stench_img, (x, y))
            elif len(cell_type) == 2 and cell_type[1] == 'B':
                self.screen.blit(self.breeze_img, (x, y))
            elif len(cell_type) == 2 and cell_type[1] == 'S':
                self.screen.blit(self.stench_img, (x, y))
            elif len(cell_type) == 2 and cell_type[1] == 'G':
                self.screen.blit(self.gold_img, (x, y))
        if cell_type == '' or cell_type == 'A':
            cell_rect = pg.Rect(x, y, space, space)
            pg.draw.rect(self.screen, BLUE, cell_rect)
        elif cell_type == 'B':
            self.screen.blit(self.breeze_img, (x, y))
        elif cell_type == 'BS':
            self.screen.blit(self.breeze_stench_img, (x, y))
        elif cell_type == 'G' or cell_type == 'BG'  or cell_type == 'GS' or cell_type == 'BGS':
            self.screen.blit(self.gold_img, (x, y))
        elif cell_type == 'P' or cell_type == 'BP' or cell_type == 'PS' or cell_type == 'BPS':
            self.screen.blit(self.pit_img, (x, y))
        elif cell_type == 'S':
            self.screen.blit(self.stench_img, (x, y))
        elif cell_type == 'W' or cell_type == 'BW':
            self.screen.blit(self.wumpus_img, (x, y))

        self.board()
            


    def arrows(self, direction, pos, world):
        row, col = pos

        x = mg_x + col * space +10
        y = mg_y + row * space +10
        
        if direction == "N":
            for r in range(row, -1, -1):
                self.screen.blit(self.arrow_img, (x, y))
        elif direction == "S":
            for r in range(row, 4):
                #prev_y = y
                y = mg_y + r * space +10
                #self.fill_env(prev_y, x, world)
                arrow_down = pg.transform.flip(self.arrow_img, False, True)
                self.screen.blit(arrow_down, (x, y))
        elif direction == "W":
            for c in range(col, -1, -1):
                x = mg_x + c * space +10
                arrow_west = pg.transform.flip(self.arrow_side_img, True, False)
                self.screen.blit(arrow_west, (x, y))
        elif direction == "E":
            for c in range(col, 4):
                x = mg_x + c * space +10
                self.screen.blit(self.arrow_side_img, (x, y))
        

    def status(self, text, color):
        text_bg = pg.Surface((240, 90))
        text_bg.fill(BLUE)
        bg_rect = text_bg.get_rect(center=(610, 350))
        pg.draw.rect(self.screen, AQUA, pg.Rect(bg_rect.left-2, bg_rect.top-2, 244, 94), 2)


        if len(text) <= 16:
            output = self.font.render(text, True, color)
            text_rect = output.get_rect(center=bg_rect.center)

            self.screen.blit(text_bg, bg_rect)
            self.screen.blit(output, text_rect)
        else:
            text_line1 = text[:16]
            text_line2 = text[16:]
            output1 = self.font.render(text_line1, True, color)
            output2 = self.font.render(text_line2, True, color)

            text_rect1 = output1.get_rect(center=(bg_rect.centerx, bg_rect.centery - 15))
            text_rect2 = output2.get_rect(center=(bg_rect.centerx, bg_rect.centery + 15))

            self.screen.blit(text_bg, bg_rect)
            self.screen.blit(output1, text_rect1)
            self.screen.blit(output2, text_rect2)

    def score(self, text, color):
        text_bg = pg.Surface((115, 60))
        text_bg.fill(LIGHT_GREEN)
        bg_rect = text_bg.get_rect(center=((680, 180)))

        output = self.font.render("Score", True, color)
        score = self.font.render(text, True, color)
        text_rect1 = score.get_rect(center=(bg_rect.centerx, bg_rect.centery + 10))
        text_rect2 = output.get_rect(center=(bg_rect.centerx, bg_rect.centery - 10))

        self.screen.blit(text_bg, bg_rect)
        self.screen.blit(score, text_rect1)
        self.screen.blit(output, text_rect2)



        

        


                    

        