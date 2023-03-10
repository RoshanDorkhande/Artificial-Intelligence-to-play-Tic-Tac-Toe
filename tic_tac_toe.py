import pygame
import copy
import sys
import random
import numpy as np
from constants import *

#initialising pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

class Board:
    def __init__(self) -> None:
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
        return 0 if no win yet (not Draw)
        return 1 if player 1 wins
        return 2 if player 2 wins
        '''
        # check vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col] #this will return the player

        # check horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0] #this will return the player
        
        # descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for rows in range(ROWS):
            for cols in range(COLS):
                if self.empty_square(rows, cols):
                    empty_sqrs.append((rows, cols))

        return empty_sqrs

    def is_full(self):
        return self.marked_sqrs == 9

    def is_empty(self):
        return self.marked_sqrs == 0
    
    
class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    # --- MINIMAX ---

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.is_full():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MAIN EVAL ---

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col
class Game:

    def __init__(self) -> None:
        self.board = Board()
        self.ai = AI()
        self.player = 1 #player 1 is cross and 2 is circle
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()
    
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):

        screen.fill(BG_COLOR)

        #verticle lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH) #first verticle Line
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQSIZE, 0), (WIDTH-SQSIZE, HEIGHT), LINE_WIDTH) #Second verticle line

        #Horizontal Lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_fig(self, row, col):
        if self.player == 1:
            #cross
            #make a descending line for the cross
            pygame.draw.line(screen, CROSS_COLOR, (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET), (
                col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE +SQSIZE -OFFSET), CROSS_WIDTH)
            # making ascending line for the cross
            pygame.draw.line(screen, CROSS_COLOR, (col * SQSIZE + OFFSET, row * SQSIZE  + SQSIZE - OFFSET), 
            (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET), CROSS_WIDTH)
            

        elif self.player == 2:
            # draw a circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
        
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def is_over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

    def game_over(self, board):
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render(f'The winner is player : {1 if board.final_state() == 1 else(0 if board.is_full() and board.final_state()== 0 else 2)}', True, 'blue')
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WIDTH//2, HEIGHT//2)
        screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()


    def reset(self):
        self.__init__()


def main():
    game = Game()
    board = game.board
    ai = game.ai

    #mainloop
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g for changing gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # 0 for random AI
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1 for random AI
                if event.key == pygame.K_1:
                    ai.level = 1

                # restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.is_over():
                        game.running =False
                        game.game_over(board)
                    
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #updating the screen to see player 1's move
            pygame.display.update()     

            # ai methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.is_over():
                game.running =False
                game.game_over(board)
                
        
        pygame.display.update()

main()