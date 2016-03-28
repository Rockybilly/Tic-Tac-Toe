"""
Basic AI implementation for tic-tac-toe
Using the Monte Carlo method.
"""

import random
from collections import defaultdict
from copy import deepcopy
from Tic import *


class MonteTicTacToe(TicTacToe):
    """
    The tic-tac-toe class inheriting from the old tic-tac-toe game.
    """

    def main(self):
        """
        The main game method, includes the main loop.
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
                        board, turn = self.board_click(deepcopy(board), mouse_pos, turn)
                        self.draw_game(screen, board, letters)
                        if self.check_win(board)[0]:
                            sleep = True
                            winner = self.check_win(board)[1] # Win evaluated twice!
                        elif turn == 1:
                            board, turn = self.move_computer(deepcopy(board), turn)
                            if self.check_win(board)[0]:
                                sleep = True
                                winner = self.check_win(board)[1] # Here too
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


    def possible_moves(self, board):
        """
        The method that returns empty squares in the board.
        """

        pos_moves = []

        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    pos_moves.append((row, col))
        return pos_moves


    def random_game(self, board, turn):
        """
        The method that takes the current board and ends it with a random result.
        """

        won, winner = self.check_win(board)
        moves = self.possible_moves(board)

        while not won:

            current_move = random.choice(moves)
            board[current_move[0]][current_move[1]] = PLAYERS[turn]

            moves.remove(current_move)
            turn = (turn + 1) % 2 # Increment team
            won, winner = self.check_win(board)

        return board, winner


    def score_board(self, board, winner):
        """
        The method that returnes the score of a certain board.
        """

        board_scores = defaultdict(int)

        if winner is None:
            return board_scores

        if winner == "O":
            for row in range(3):
                for col in range(3):
                    #if board[row][col] == 0:
                        #board_scores[(row, col)]
                    if board[row][col] == "X":
                        board_scores[(row, col)] -= 1
                    elif board[row][col] == "O":
                        board_scores[(row, col)] += 1
        elif winner == "X":
            for row in range(3):
                for col in range(3):
                    #if board[row][col] == 0:
                        #board_scores[(row, col)]
                    if board[row][col] == "X":
                        board_scores[(row, col)] += 1
                    elif board[row][col] == "O":
                        board_scores[(row, col)] -= 1

        return board_scores


    def update_grid_scores(self, board_scores, new_scores):
        """
        The method that updates stored board scores given the new scores.
        """

        for key in new_scores:
            board_scores[key] += new_scores[key]

        return board_scores


    def get_best_move(self, board, board_scores):
        """
        The method that finds best move to make using the board scores we assinged
        at random_game method.
        """

        moves = self.possible_moves(board)

        sorted_moves = sorted(board_scores, key=lambda x: board_scores[x], reverse=True)

        if sorted_moves == []:
            return random.choice(moves)

        for move in sorted_moves:
            if move in moves:
                return move


    def move_computer(self, board, turn):
        """
        The method that makes that computer play using the best move returned.
        """
        
        trial_number = 5000 # Hardness level
        board_scores = defaultdict(int)

        for _ in xrange(trial_number):
            ended_rand_game, rand_winner = self.random_game(deepcopy(board), turn)
            board_scores = self.update_grid_scores(board_scores, self.score_board(ended_rand_game, rand_winner))
        
        move = self.get_best_move(board, board_scores)

        board[move[0]][move[1]] = PLAYERS[turn]
        turn = (turn + 1) % 2 # Increment team

        #time.sleep(0.5)
        return board, turn


if __name__ == "__main__":
    game = MonteTicTacToe()
    game.main()
