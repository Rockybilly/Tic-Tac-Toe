"""
Tic-Tac-Toe Implementation.
Two-Player Version No AI.
"""

import sys
import time
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SIZE = 420 # Screen size
INTERVAL = SIZE / 3
PLAYERS = ["X", "O"]

pygame.display.set_caption("Tic Tac Toe")

class TicTacToe(object):
    """
    The Class for the game.
    """
    
    def main(self):
        """
        The main game function, includes the main loop.
        """
        
        pygame.init()

        screen = pygame.display.set_mode((SIZE, SIZE)) # Initializing square scree
        letters = pygame.image.load("XO.png")

        gamemode = "game"
        sleep = False

        board = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

        turn = 0

        while True: # The main game loop.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if gamemode == "game":
                        board, turn = self.board_click(board, mouse_pos, turn)
                        if self.check_win(board)[0]:
                            sleep = True
                            winner = self.check_win(board)[1] # Win evaluated twice, should not use on larger lists.

                    elif gamemode == "end":
                        board, turn, gamemode, winner = self.end_click(board, turn, gamemode, mouse_pos, winner)

            if gamemode == "game":
                self.draw_game(screen, board, letters)
                if sleep: # One second waiting after game finishes.
                    time.sleep(1)
                    gamemode = "end"
                    sleep = False
            elif gamemode == "end":
                self.draw_end_game(screen, winner)

    def board_click(self, board, pos, turn):
        """
        The function to change board using the mouse position input.
        """

        row, col = pos[1] / INTERVAL, pos[0] / INTERVAL
        if board[row][col] == 0: # Preventing selecting same square twice
            board[row][col] = PLAYERS[turn]
            turn = (turn + 1) % 2 # Increment team  
        return board, turn

    def end_click(self, board, turn, gamemode, pos, winner):
        """
        The function to restart the game using mouse input(Restart Button).
        """

        if 85 <= pos[0] <= 355 and 300 <= pos[1] <= 360:
            board = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]
            turn = 0
            gamemode = "game"
            winner = None

        return board, turn, gamemode, winner

    def check_win(self, board):
        """
        The function to check winning conditions.
        """

        won = False
        winner = None

        for row in board: # Check rows
            values = set(row)
            if len(values) == 1 and 0 not in values:
                won = True
                winner = list(values)[0]
                return won, winner

        for col in zip(*board): # Check columns
            values = set(col)
            if len(values) == 1 and 0 not in values:
                won = True
                winner = list(values)[0]
                return won, winner        

        values = set([board[0][0], board[1][1], board[2][2]])
        if len(values) == 1 and 0 not in values: # Check main diagonal
            won = True
            winner = list(values)[0]
            return won, winner

        values = set([board[0][2], board[1][1], board[2][0]])
        if len(values) == 1 and 0 not in values: # Check anti main diagonal
            won = True
            winner = list(values)[0]
            return won, winner

        finished = all([True if 0 not in row else False for row in board]) # Checking if the board is full.

        if finished and not won: # Table full, but no winner.
            won = True # Not won, but a Tie.

        return won, winner

    def draw_game(self, surface, board, letters):
        """
        The function that draws main game to the screen.
        """

        line_width = 2

        surface.fill(WHITE)

        for pos in range(INTERVAL, SIZE - SIZE%3, INTERVAL): # Draw board
            pygame.draw.line(surface, BLACK, (pos, 0), (pos, SIZE), line_width) # Horizontal lines
            pygame.draw.line(surface, BLACK, (0, pos), (SIZE, pos), line_width) # Vertical lines

        for row in range(3): # Draw letters
            for col in range(3):
                value = board[row][col]
                if value != 0:
                    ind = PLAYERS.index(value)
                    surface.blit(letters, (col*INTERVAL + 5, row*INTERVAL + 5), (ind*INTERVAL, 0, 120, 120))

        pygame.display.flip()

    def draw_end_game(self, surface, winner):
        """
        The function that draws end game to the screen.
        """

        over_font = pygame.font.SysFont("monospace", 60)
        winner_font = pygame.font.SysFont("monospace", 25)
        surface.fill(BLACK)

        if winner == "X":
            surface.blit(over_font.render("Game Over!", 20, WHITE), (38, 60))
            surface.blit(winner_font.render("X is the victor.", 10, WHITE), (90, 150))
        elif winner == "O":
            surface.blit(over_font.render("Game Over!", 20, WHITE), (38, 60))
            surface.blit(winner_font.render("O is the victor.", 10, WHITE), (90, 150))
        elif winner == None:
            surface.blit(over_font.render("It's a Tie!", 20, WHITE), (20, 60))
                  
        pygame.draw.rect(surface, RED ,(85, 300, 260, 60), 2)
        surface.blit(winner_font.render("RESTART ?", 25, GREEN), (155, 315))
        pygame.display.flip()


if __name__ == "__main__":
    game = TicTacToe()
    game.main()
