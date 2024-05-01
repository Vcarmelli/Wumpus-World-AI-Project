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
pg.display.set_caption("Wumpus World (Space Edition) by VKVC")

def generate_board():
    board = np.zeros((4, 4))
    return board

def get_coord(pos):
    dif = 400 / 4
    x = pos[0]//dif
    y = pos[1]//dif
    return [y, x]

def over():
    draw = Draw(screen)

    while True:
        
        MOUSE_POS = pg.mouse.get_pos()
        btn_reset = Button((550, 250), " Reset ", GREEN, LIGHT_GREEN)
        btn_back = Button((680, 250), " Menu ", GREEN, LIGHT_GREEN)

        for button in [btn_reset, btn_back]:
            button.update_color(MOUSE_POS)
            button.draw_button(screen)

        for event in pg.event.get():
            
            if event.type == pg.QUIT: sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                    
                    if btn_reset.click_button(MOUSE_POS):
                        wumpus_world()

                    if btn_back.click_button(MOUSE_POS):
                        main()

        draw.board()
        pg.display.flip()

def wumpus_world():
    pg.event.clear()

    draw = Draw(screen)
    ww = WumpusWorld()
    ww.prepare_environment()
    
    game_bg = pg.image.load("assets/game-bg.png")
    screen.blit(game_bg, (0,0)) 
    grabbed = killed = False   
    while True:
        
        MOUSE_POS = pg.mouse.get_pos()

        btn_ai = Button((550, 180), "Play AI", GREEN, LIGHT_GREEN)
        btn_reset = Button((550, 250), " Reset ", GREEN, LIGHT_GREEN)
        btn_back = Button((680, 250), " Menu ", GREEN, LIGHT_GREEN)
       
        for button in [btn_ai, btn_reset, btn_back]:
            button.update_color(MOUSE_POS)
            button.draw_button(screen)
            
        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)        
        for event in pg.event.get():
            
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                
                if btn_reset.click_button(MOUSE_POS):
                    wumpus_world()

                if btn_back.click_button(MOUSE_POS):
                    main()

                if btn_ai.click_button(MOUSE_POS):
                    while True:
                        ww.cur_row, ww.cur_col = ww.agent.get_move(ww.agent.has_gold)
                        ww.agent.direction(ww.cur_row, ww.cur_col)
                        draw.fill_env(ww.cur_row, ww.cur_col, ww.world)  
                        ww.move_agent(ww.cur_row, ww.cur_col)
                        ww.path[ww.cur_row][ww.cur_col] = 1     

                        pg.time.delay(500)
                        draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
                        draw.score(f"{ww.agent.score}", GREEN)
                        for row in range(4):
                            for col in range(4):
                                if ww.path[row][col]:
                                    draw.fill_env(row, col, ww.world)
                                draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
                                
                        
                        stats = ww.game_status()
                        print("STATs:", stats)
                        if stats == -1:
                            draw.status("Game is ongoing!", LIGHT_GREEN)            
                        elif stats == 0 and not grabbed:
                            draw.status(" You found the  golden treasure!", WHITE)                  
                            ww.world = ww.agent.grab(ww.cur_row, ww.cur_col, ww.world)
                            draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
                            #draw.fill_env(ww.cur_row, ww.cur_col, ww.world)  
                            ww.g_w_p_coords[0] = None
                            pg.display.update()
                            grabbed = True
                        elif stats == 1:
                            draw.status(" Game over. You met the Wumpus!", WHITE) 
                            draw.environment(ww.world)
                            over()
                        elif 2 <= stats < 5:
                            draw.status(" Game over. You fall into the pit!", WHITE) 
                            draw.environment(ww.world)
                            over()
                        elif stats == 9 and ww.agent.location == (0, 0):
                            draw.status("   Agent win!   Congratulations!", WHITE) 
                            draw.environment(ww.world)
                            draw.agent(ww.cur_row, ww.cur_col, 'V')  
                            over()
                        elif stats == 10 and not killed:
                            draw.fill_env(ww.agent.w_pos[0], ww.agent.w_pos[1], ww.world)  
                            draw.arrows(ww.agent.facing, ww.agent.location, ww.world)
                            ww.agent.w_found = False
                            ww.g_w_p_coords[1] = None
                            draw.status(" Wumpus scream! You killed Wumpus.", WHITE)  
                            pg.display.update()
                            killed = True   
                        elif grabbed and killed:
                            draw.status(" Treasure found and Wumpus killed!", AQUA) 
                        else:
                            draw.status("Game is ongoing!", LIGHT_GREEN)         

                        pg.display.update()
                        
            
        #     if event.type == pg.KEYDOWN:
        #         if event.key == pg.K_RIGHT:
        #             if ww.cur_col < 3:
        #                 ww.cur_col += 1
        #                 draw.fill_env(ww.cur_row, ww.cur_col, ww.world)  
        #                 ww.move_agent(ww.cur_row, ww.cur_col)
        #         elif event.key == pg.K_LEFT:
        #             if ww.cur_col > 0:
        #                 ww.cur_col -= 1
        #                 draw.fill_env(ww.cur_row, ww.cur_col, ww.world)   
        #                 ww.move_agent(ww.cur_row, ww.cur_col)
        #         elif event.key == pg.K_DOWN:
        #             if ww.cur_row < 3:
        #                 ww.cur_row += 1
        #                 draw.fill_env(ww.cur_row, ww.cur_col, ww.world)  
        #                 ww.move_agent(ww.cur_row, ww.cur_col)
        #         elif event.key == pg.K_UP:
        #             if ww.cur_row > 0:
        #                 ww.cur_row -= 1
        #                 draw.fill_env(ww.cur_row, ww.cur_col, ww.world)   
        #                 ww.move_agent(ww.cur_row, ww.cur_col)
   
                
        #         ww.path[ww.cur_row][ww.cur_col] = 1   

        # for row in range(4):
        #     for col in range(4):
        #         if ww.path[row][col]:
        #             draw.fill_env(row, col, ww.world)
        #         draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)    

        draw.score(f"{ww.agent.score}", GREEN)
        draw.status("Click the 'Play AI' button!", WHITE)    
        
        draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
        
        
        draw.board()
        pg.display.flip()


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
        
        pg.display.flip()



def main():
    menu_bg = pg.image.load("assets/background.png")
    screen.blit(menu_bg, (0,0))

    while True:

        MOUSE_POS = pg.mouse.get_pos()

        start = Button((370, 480), "Start Game", BLUE, LIGHT_GREEN)
        controls = Button((485, 480), " ? ", BLUE, LIGHT_GREEN)
       
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

        pg.display.flip()
    
    

if __name__ == "__main__":
    main()