import random
import time
import pygame

pygame.init()

RED = (255,0,0)
ORANGE = (255,127,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
GREY = (127,127,127)
BLACK = (0,0,0)

size = (600,700)
square_width_height = 40
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Minesweeper")

done = False
ROWS_COLS = 15
MINES = 30

clock = pygame.time.Clock()

font = pygame.font.Font(None,20)

gameState = -1


def infoBar():
    global gameState
    pygame.draw.rect(screen,GREY,(0,0,600,100))
    pygame.draw.line(screen,BLACK,(0,100),(600,100),4)
    
    if gameState == 0:
        text = font.render("MINES: " + str(game.nummines),True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((150 - (text_x / 2)),(50 - (text_y / 2))))
        text = font.render("FLAGS: " + str(game.numflaged),True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((350 - (text_x / 2)),(50 - (text_y / 2))))
    elif gameState == 1:      #win
        text = font.render("YOU  WIN",True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((150 - (text_x / 2)),(50 - (text_y / 2))))
    elif gameState == 2:    #loose
        text = font.render("YOU  LOSE",True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((150 - (text_x / 2)),(50 - (text_y / 2))))

    

class Tile():
    def __init__(self,column,row):
        # self.probability = -1
        self.column = column
        self.row = row
        self.mine = False
        self.neighbors = 0
        self.visible = False
        self.flag = False
        self.complete = False
        self.left = row*square_width_height
        self.top = (column*square_width_height)+100
    
    def update(self, agent):
        global gameState
        if gameState == 0:
            if agent.flag_state == False and agent.chosen_row == self.row and agent.chosen_col == self.column:
                self.visible = True
                self.flag = agent.flag_state
            if agent.flag_state == True and agent.chosen_row == self.row and agent.chosen_col == self.column:
                if self.flag == False:
                    self.flag = True
                elif self.flag == True:
                    self.flag = False
            if self.visible == True and self.mine == True:
                gameState = 2
    
    def show(self):
        rect = (self.left,self.top,square_width_height,square_width_height)
        if self.flag == True:
            pygame.draw.rect(screen,YELLOW,rect)
        if self.visible == True:
            if self.mine == False:
                pygame.draw.rect(screen,GREY,rect)
                if self.neighbors > 0:
                    text = font.render(str(self.neighbors),True,BLACK)
                    text_x = text.get_rect().width
                    text_y = text.get_rect().height
                    screen.blit(text,((self.left + (square_width_height / 2) - (text_x / 2)),(self.top + (square_width_height / 2) - (text_y / 2))))
            
            elif self.mine == True:
                pygame.draw.rect(screen,RED,rect)
        
        pygame.draw.rect(screen,BLACK,rect,2)

class Game():
    def __init__(self,columns,rows,mines):
        self.columns = columns
        self.rows = rows
        self.nummines = mines
        self.board = []
        self.mines = []
        self.minenum = len(self.mines)
        self.neighbnum = 0
        self.numflaged = 0
        self.numvis = 0
        self.foundmines = 0
        
        #creating board
        for y in range(self.rows):
            self.board.append([])
            for x in range(self.columns):
                self.board[y].append(Tile(x,y))
        
        #placing mines
        while self.minenum < self.nummines:
            self.mineloc = [random.randrange(self.columns),random.randrange(self.rows)]
            if self.board[self.mineloc[1]][self.mineloc[0]].mine == False:
                self.mines.append(self.mineloc)
                self.board[self.mineloc[1]][self.mineloc[0]].mine = True
            self.minenum = len(self.mines)
        
        #neighbors
        for y in range(self.rows):
            for x in range(self.columns):
                self.neighbnum = 0
                if y > 0 and x > 0:
                    if self.board[y-1][x-1].mine == True:
                        self.neighbnum += 1
                if y > 0:
                    if self.board[y-1][x].mine == True:
                        self.neighbnum += 1
                if y > 0 and x < (self.columns - 1):
                    if self.board[y-1][x+1].mine == True:
                        self.neighbnum += 1
                if x > 0:
                    if self.board[y][x-1].mine == True:
                        self.neighbnum += 1
                if x < (self.columns - 1):
                    if self.board[y][x+1].mine == True:
                        self.neighbnum += 1
                if x > 0 and y < (self.rows - 1):
                    if self.board[y+1][x-1].mine == True:
                        self.neighbnum += 1
                if y < (self.rows - 1):
                    if self.board[y+1][x].mine == True:
                        self.neighbnum += 1
                if x < (self.columns - 1) and y < (self.rows - 1):
                    if self.board[y+1][x+1].mine == True:
                        self.neighbnum += 1
                self.board[y][x].neighbors = self.neighbnum
    
    def update(self, agent):
        global gameState
        self.numflaged = 0
        self.numvis = 0
        self.foundmines = 0
        for y in range(self.rows):
            for x in range(self.columns):
                self.board[y][x].update(agent)
                if self.board[y][x].neighbors == 0 and self.board[y][x].visible == True:
                    if y > 0 and x > 0:
                        self.board[y-1][x-1].visible = True
                    if y > 0:
                        self.board[y-1][x].visible = True
                    if y > 0 and x < (self.columns - 1):
                        self.board[y-1][x+1].visible = True
                    if x > 0:
                        self.board[y][x-1].visible = True
                    if x < (self.columns - 1):
                        self.board[y][x+1].visible = True
                    if x > 0 and y < (self.rows - 1):
                        self.board[y+1][x-1].visible = True
                    if y < (self.rows - 1):
                        self.board[y+1][x].visible = True
                    if x < (self.columns - 1) and y < (self.rows - 1):
                        self.board[y+1][x+1].visible = True
                if self.board[y][x].flag == True:
                    self.numflaged += 1
                if self.board[y][x].visible == True:
                    self.numvis += 1
        for mine in self.mines:
            if self.board[mine[1]][mine[0]].flag == True:
                self.foundmines += 1
        if self.numflaged == self.nummines and self.foundmines == self.nummines and self.numvis == ((self.columns * self.rows) - self.nummines):
            gameState = 1
        if gameState == 1 or gameState == 2:
            for y in range(self.rows):
                for x in range(self.columns):
                    self.board[y][x].visible = True
        
    
    def render(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.board[y][x].show()

class Agent:
    def __init__(self):
        self.flag_state = False
        self.chosen_col = 0
        self.chosen_row = 0
        self.current_mine_count = 0
        self.mines_flagged = 0
    def process_squares(self, game_setup):
        num_squares = 0
        for row in range(ROWS_COLS):
            for col in range(ROWS_COLS):
                # time.sleep(2)
                if game_setup.board[row][col].visible and not game_setup.board[row][col].complete\
                    and game_setup.board[row][col].neighbors:
                    self.chosen_col = col
                    self.chosen_row = row
                    self.current_mine_count = game_setup.board[row][col].neighbors
                    probability = self.find_prob(game_setup)
                    print("Prob:" + str(probability))
                    if probability == 1:
                        self.flag_all_neighbors(game_setup)
                        game_setup.board[row][col].complete = True
                        num_squares += 1
                        screen.fill(WHITE)
                        infoBar()
                        game.update(self)
                        game.render()
                        pygame.display.flip()
                        clock.tick(60)
                    elif probability == 0:
                        self.show_all_neighbors(game_setup)
                        game_setup.board[row][col].complete = True
                        num_squares += 1
                        screen.fill(WHITE)
                        infoBar()
                        game.update(self)
                        game.render()
                        pygame.display.flip()
                        clock.tick(60)
        return num_squares
    
    # def move_right(self, game_setup):
    #     if self.chosen_col == 14 or not game_setup.board[self.chosen_row][self.chosen_col].visible:
    #         return
    #     # game_setup.board[self.chosen_row][self.chosen_col].probability = 0
    #     while self.chosen_col+1 < ROWS_COLS and game_setup.board[self.chosen_row][self.chosen_col+1].visible:
    #         self.chosen_col += 1
    #         if game_setup.board[self.chosen_row][self.chosen_col].neighbors:
    #             self.current_mine_count = game_setup.board[self.chosen_row][self.chosen_col].neighbors
    #             probability = self.find_prob(game_setup)
    #             if probability == 1:
    #                 print("Flagged: " + str(self.chosen_col) + ", " + str(self.chosen_row))
    #                 self.flag_all_neighbors(game_setup)
    #             elif probability == 0:
    #                 print("Show: " + str(self.chosen_col) + ", " + str(self.chosen_row))
    #                 self.show_all_neighbors(game_setup)

    # def move_down(self, game_setup):
    #     if self.chosen_col == 14 or not game_setup.board[self.chosen_row][self.chosen_col].visible:
    #         return
    #     while self.chosen_row+1 < ROWS_COLS and game_setup.board[self.chosen_row+1][self.chosen_col].visible:
    #         self.chosen_row += 1
    #         if game_setup.board[self.chosen_row][self.chosen_col].neighbors:
    #             self.current_mine_count = game_setup.board[self.chosen_row][self.chosen_col].neighbors
    #             probability = self.find_prob(game_setup)
    #             if probability == 1:
    #                 self.flag_all_neighbors(game_setup)
    #             elif probability == 0:
    #                 self.show_all_neighbors(game_setup)
        

    def show_all_neighbors(self, game_setup):
        self.flag_state = False
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col+1 < ROWS_COLS:
            game_setup.board[self.chosen_row+1][self.chosen_col+1].visible = True
        if self.chosen_col+1 < ROWS_COLS:
            game_setup.board[self.chosen_row][self.chosen_col+1].visible = True
        if self.chosen_row+1 < ROWS_COLS:
            game_setup.board[self.chosen_row+1][self.chosen_col].visible = True
        if self.chosen_row-1 >= 0 and self.chosen_col-1 >= 0:
            game_setup.board[self.chosen_row-1][self.chosen_col-1].visible = True
        if self.chosen_col-1 >= 0:
            game_setup.board[self.chosen_row][self.chosen_col-1].visible = True
        if self.chosen_row-1 >= 0:
            game_setup.board[self.chosen_row-1][self.chosen_col].visible = True
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col-1 >= 0:
            game_setup.board[self.chosen_row+1][self.chosen_col-1].visible = True
        if self.chosen_row-1 >= 0 and self.chosen_col+1 < ROWS_COLS:
            game_setup.board[self.chosen_row-1][self.chosen_col+1].visible = True
        
    def flag_all_neighbors(self, game_setup):
        self.flag_state = True
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col+1 < ROWS_COLS:
            game_setup.board[self.chosen_row+1][self.chosen_col+1].flag = True
        if self.chosen_col+1 < ROWS_COLS:
            game_setup.board[self.chosen_row][self.chosen_col+1].flag = True
        if self.chosen_row+1 < ROWS_COLS:
            game_setup.board[self.chosen_row+1][self.chosen_col].flag = True
        if self.chosen_row-1 >= 0 and self.chosen_col-1 >= 0:
            game_setup.board[self.chosen_row-1][self.chosen_col-1].flag = True
        if self.chosen_col-1 >= 0:
            game_setup.board[self.chosen_row][self.chosen_col-1].flag = True
        if self.chosen_row-1 >= 0:
            game_setup.board[self.chosen_row-1][self.chosen_col].flag = True
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col-1 >= 0:
            game_setup.board[self.chosen_row+1][self.chosen_col-1].flag = True
        if self.chosen_row-1 >= 0 and self.chosen_col+1 < ROWS_COLS:
            game_setup.board[self.chosen_row-1][self.chosen_col+1].flag = True        
    
    def find_prob(self, game_setup):
        total = self.current_mine_count
        total_hidden = 8
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col+1 < ROWS_COLS and game_setup.board[self.chosen_row+1][self.chosen_col+1].flag:
            total -= 1
        if self.chosen_col+1 < ROWS_COLS and game_setup.board[self.chosen_row][self.chosen_col+1].flag:
            total -= 1
        if self.chosen_row+1 < ROWS_COLS and game_setup.board[self.chosen_row+1][self.chosen_col].flag:
            total -= 1
        if self.chosen_row-1 >= 0 and self.chosen_col-1 >= 0 and game_setup.board[self.chosen_row-1][self.chosen_col-1].flag:
            total -= 1
        if self.chosen_col-1 >= 0 and game_setup.board[self.chosen_row][self.chosen_col-1].flag:
            total -= 1
        if self.chosen_row-1 >= 0 and game_setup.board[self.chosen_row-1][self.chosen_col].flag:
            total -= 1
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col-1 >= 0 and game_setup.board[self.chosen_row+1][self.chosen_col-1].flag:
            total -= 1
        if self.chosen_row-1 >= 0 and self.chosen_col+1 < ROWS_COLS and game_setup.board[self.chosen_row-1][self.chosen_col+1].flag:
            total -= 1
        
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col+1 < ROWS_COLS and game_setup.board[self.chosen_row+1][self.chosen_col+1].visible:
            total_hidden -= 1
        if self.chosen_col+1 < ROWS_COLS and game_setup.board[self.chosen_row][self.chosen_col+1].visible:
            total_hidden -= 1
        if self.chosen_row+1 < ROWS_COLS and game_setup.board[self.chosen_row+1][self.chosen_col].visible:
            total_hidden -= 1
        if self.chosen_row-1 >= 0 and self.chosen_col-1 >= 0 and game_setup.board[self.chosen_row-1][self.chosen_col-1].visible:
            total_hidden -= 1
        if self.chosen_col-1 >= 0 and game_setup.board[self.chosen_row][self.chosen_col-1].visible:
            total_hidden -= 1
        if self.chosen_row-1 >= 0 and game_setup.board[self.chosen_row-1][self.chosen_col].visible:
            total_hidden -= 1
        if self.chosen_row+1 < ROWS_COLS and self.chosen_col-1 >= 0 and game_setup.board[self.chosen_row+1][self.chosen_col-1].visible:
            total_hidden -= 1
        if self.chosen_row-1 >= 0 and self.chosen_col+1 < ROWS_COLS and game_setup.board[self.chosen_row-1][self.chosen_col+1].visible:
            total_hidden -= 1
        
        if not total or not total_hidden:
            return 0
        return total/total_hidden




if __name__ == "__main__":
    game = Game(ROWS_COLS,ROWS_COLS,MINES)
    gameState = 0
    agent = Agent()
    
    while not done:
        events = pygame.event.get()
        if events and events[0].type == pygame.QUIT:
            done = True
        else:
            num = agent.process_squares(game)
            if not num:
                print("Not: " + str(agent.chosen_col) + ", " + str(agent.chosen_row))
                row = random.randrange(ROWS_COLS-1)
                col = random.randrange(ROWS_COLS-1)
                game.board[row][col].visible = True
    
        screen.fill(WHITE)
        infoBar()
        
        game.update(agent)
        game.render()
    
        pygame.display.flip()
    
        clock.tick(60)
        if gameState  == 1 or gameState ==2:
            done = True
    while not events:
        None
    pygame.quit()