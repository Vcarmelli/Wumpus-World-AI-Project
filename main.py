import sys, pygame as pg
import numpy as np
from button import Button
from draw import Draw
from game import WumpusWorld

pg.init()

space = 85

AQUA = (49, 255, 255)
WHITE = (255, 255, 255)
GREEN = (67, 83, 24)
LIGHT_GREEN = (194, 203, 159)
BLUE = (6, 61, 81)
TRANSPARENT = (0, 0, 0, 255)


screen = pg.display.set_mode((780, 550))
pg.display.set_caption("Wumpus World")

def generate_board():
    board = np.zeros((4, 4))
    return board

def get_coord(pos):
    dif = 400 / 4
    x = pos[0]//dif
    y = pos[1]//dif
    return [y, x]

def wumpus_world():
    draw = Draw(screen)
    ww = WumpusWorld()
    
    game_bg = pg.image.load("assets/game-bg.png")
    screen.blit(game_bg, (0,0))
    
    ww.prepare_environment()
    while True:
        
        MOUSE_POS = pg.mouse.get_pos()

        btn_ai = Button((570, 230), "Play AI", BLUE, LIGHT_GREEN)
        btn_reset = Button((570, 300), "Reset Game", BLUE, LIGHT_GREEN)
        btn_back = Button((570, 370), "Menu", BLUE, LIGHT_GREEN)
       
        for button in [btn_ai, btn_reset, btn_back]:
            button.update_color(MOUSE_POS)
            button.draw_button(screen)

        for event in pg.event.get():
            
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                
                if btn_reset.click_button(MOUSE_POS):
                    wumpus_world()

                if btn_back.click_button(MOUSE_POS):
                    main()

                if btn_ai.click_button(MOUSE_POS):
                    row, col = ww.agent.get_move()
                    draw.fill_env(row, col, ww.world)  
                    ww.move_agent(row, col)
                    ww.path[row][col] = 1     

            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    if ww.cur_col < 3:
                        ww.cur_col += 1
                        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)  
                        ww.move_agent(ww.cur_row, ww.cur_col)
                elif event.key == pg.K_LEFT:
                    if ww.cur_col > 0:
                        ww.cur_col -= 1
                        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)   
                        ww.move_agent(ww.cur_row, ww.cur_col)
                elif event.key == pg.K_DOWN:
                    if ww.cur_row < 3:
                        ww.cur_row += 1
                        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)  
                        ww.move_agent(ww.cur_row, ww.cur_col)
                elif event.key == pg.K_UP:
                    if ww.cur_row > 0:
                        ww.cur_row -= 1
                        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)   
                        ww.move_agent(ww.cur_row, ww.cur_col)
   
                #draw.agent(ww.cur_row, ww.cur_col)  
                ww.path[ww.cur_row][ww.cur_col] = 1     

            for row in range(4):
                for col in range(4):
                    if ww.path[row][col]:
                        draw.fill_env(row, col, ww.world)
                    
                     
        
        draw.board()
        pg.display.update()

def description():
    game_bg = pg.image.load("assets/description-bg.png")
    screen.blit(game_bg, (0,0))
    
    while True:
        
        MOUSE_POS = pg.mouse.get_pos()

        btn_back = Button((710, 490), "Back \u25BA", BLUE, LIGHT_GREEN)
       
        btn_back.update_color(MOUSE_POS)
        btn_back.draw_button_transparent(screen)

        for event in pg.event.get():
            
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:

                if btn_back.click_button(MOUSE_POS):
                    main()
        
        pg.display.update()



def main():
    menu_bg = pg.image.load("assets/background.png")
    screen.blit(menu_bg, (0,0))

    while True:

        MOUSE_POS = pg.mouse.get_pos()

        start = Button((370, 480), "Start Game", BLUE, LIGHT_GREEN)
        controls = Button((485, 480), "?", BLUE, LIGHT_GREEN)
       
        for button in [start, controls]:
            button.update_color(MOUSE_POS)
            start.draw_button(screen)
            controls.draw_button_transparent(screen)

        for event in pg.event.get():
            
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if start.click_button(MOUSE_POS):
                    wumpus_world()

                if controls.click_button(MOUSE_POS):
                    description()

        pg.display.update()
    
    

if __name__ == "__main__":
    main()