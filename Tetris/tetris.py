#
# This is a Terminal based Tetris game
#
# Coded by Amir otd :)[https://github.com/amirotd]

import os
import sys
import select
import tty
import termios
import random
import time
from copy import deepcopy


class Tetris:
    def __init__(self):
        self.o = [[1, 1],
                  [1, 1]]

        self.i = [[1], [1], [1], [1]]

        self.Z = [[1, 1, 0],
                  [0, 1, 1]]

        self.S = [[0, 1, 1],
                  [1, 1, 0]]

        self.T = [[0, 1, 0],
                  [1, 1, 1]]

        self.L = [[1, 0],
                  [1, 0],
                  [1, 1]]

        self.J = [[0, 1],
                  [0, 1],
                  [1, 1]]

        self.pieces = [self.S, self.Z, self.i, self.o, self.J, self.L, self.T]
        self.board = [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                      [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]

    @staticmethod
    def clear_screen():
        os.system('clear')

    def print_board(self, current_piece, piece_pos, next_piece, score):
        self.clear_screen()
        board_copy = deepcopy(self.board)
        m = 0
        current_piece_size_y = len(current_piece)
        current_piece_size_x = len(current_piece[0])
        for i in range(current_piece_size_y):
            for j in range(current_piece_size_x):
                board_copy[piece_pos[0]+i][piece_pos[1]+j] = current_piece[i][j] | self.board[piece_pos[0]+i][piece_pos[1]+j]

        print("")
        print(" " * 10 + "\033[1;32m =" * 12)
        for i in range(22):
            print(" " * 10, end='')
            for j in range(12):
                if board_copy[i][j] == 1:
                    print("▌▌", end='')
                elif board_copy[i][j] == 2:
                    print("|+|", end='')
                elif board_copy[i][j] == 3:
                    print(" =", end='')
                else:
                    print("..", end='')

            if i == 5:
                print("   Next Piece:", end='')
            if 6 < i < 11:  # print next piece
                print(" " * 5, end='')
                for n in range(len(next_piece[0])):
                    if len(next_piece) > m:
                        if next_piece[m][n] == 1:
                            print("▌▌", end='')
                        else:
                            print("  ", end='')
                m += 1
            if i == 15:
                print("   Score: {0}".format(score), end='')

            print("")

    def get_piece(self):
        return random.choice(self.pieces)

    @staticmethod
    def get_down(piece_pos):
        new_piece_pos = [piece_pos[0] + 1, piece_pos[1]]
        return new_piece_pos

    @staticmethod
    def get_left(piece_pos):
        new_piece_pos = [piece_pos[0], piece_pos[1] - 1]
        return new_piece_pos

    @staticmethod
    def get_right(piece_pos):
        new_piece_pos = [piece_pos[0], piece_pos[1] + 1]
        return new_piece_pos

    @staticmethod
    def rotate_piece(piece):
        piece_copy = deepcopy(piece)
        reverse_piece = piece_copy[::-1]
        return list(list(i) for i in zip(*reverse_piece))

    def piece_to_board_collision(self, current_piece, piece_pos):
        current_piece_size_y = len(current_piece)
        current_piece_size_x = len(current_piece[0])
        for i in range(current_piece_size_y):
            for j in range(current_piece_size_x):
                self.board[piece_pos[0]+i][piece_pos[1]+j] = current_piece[i][j] | self.board[piece_pos[0]+i][piece_pos[1]+j]

    def check_collision(self, current_piece, piece_pos):
        current_piece_size_y = len(current_piece)
        current_piece_size_x = len(current_piece[0])
        for i in range(current_piece_size_y):
            for j in range(current_piece_size_x):
                if self.board[piece_pos[0] + i][piece_pos[1] + j] in (1, 2, 3) and current_piece[i][j] == 1:
                    return False
        return True

    def valid_left(self, current_piece, piece_pos):
        piece_pos = self.get_left(piece_pos)
        return self.check_collision(current_piece, piece_pos)

    def valid_right(self, current_piece, piece_pos):
        piece_pos = self.get_right(piece_pos)
        return self.check_collision(current_piece, piece_pos)

    def valid_down(self, current_piece, piece_pos):
        piece_pos = self.get_down(piece_pos)
        return self.check_collision(current_piece, piece_pos)

    def valid_rotate(self, current_piece, piece_pos):
        current_piece = self.rotate_piece(current_piece)
        return self.check_collision(current_piece, piece_pos)

    def clear_rows(self):
        filled_rows = 0

        for row in self.board:
            if row == [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]:
                filled_rows += 1

        score = filled_rows * 10

        for i in range(filled_rows):
            self.board.remove([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
            self.board.insert(0, [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2])

        return score

    def game_over(self, current_piece, piece_pos):
        if not self.valid_down(current_piece, piece_pos) and piece_pos[0] == 0:
            return True
        return False

    @staticmethod
    def kbhit():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def main(self):
        change_piece = False
        current_piece = self.get_piece()
        next_piece = self.get_piece()
        piece_pos = [0, 4]
        score = 0
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())

            self.clear_screen()
            input("""\033[1;34m
                                  _____  ___  _____  ___  ___  ___ 
                                 |_   _|| __||_   _|| _ \|_ _|/ __|
                                   | |  | _|   | |  |   / | | \__ \\
                                   |_|  |___|  |_|  |_|_\|___||___/  
                                                                   by @amirotd

                                [*] Press ENTER to start...
                        """)
            while not self.game_over(current_piece, piece_pos):
                if self.kbhit():
                    c = sys.stdin.read(1)
                    if c == 'w':
                        if self.valid_rotate(current_piece, piece_pos):
                            current_piece = self.rotate_piece(current_piece)
                    if c == 'a':
                        if self.valid_left(current_piece, piece_pos):
                            piece_pos = self.get_left(piece_pos)
                    if c == 'd':
                        if self.valid_right(current_piece, piece_pos):
                            piece_pos = self.get_right(piece_pos)
                    if c == 's':
                        if self.valid_down(current_piece, piece_pos):
                            piece_pos = self.get_down(piece_pos)
                    if c == 'q':
                        break

                if self.valid_down(current_piece, piece_pos):
                    piece_pos = self.get_down(piece_pos)

                if not self.valid_down(current_piece, piece_pos):
                    self.piece_to_board_collision(current_piece, piece_pos)
                    score += self.clear_rows()
                    change_piece = True

                if change_piece:
                    current_piece = next_piece
                    next_piece = self.get_piece()
                    piece_pos = [0, 4]
                    change_piece = False

                self.print_board(current_piece, piece_pos, next_piece, score)
                time.sleep(0.3)

        finally:
            self.clear_screen()
            print("""\033[0;31m 
                                              ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
                                              ▌     ___    _    _    _  ___     ▌
                                              ▌    / __|  /_\  | \  / || __|    ▌
                                              ▌   | (_ | / _ \ | |\/| || _|     ▌
                                              ▌    \___|/_/ \_\|_|  |_||___|    ▌
                                              ▌     ___ _    _  ___  ___  _     ▌
                                              ▌    / _ \\\ \ / /| __|| _ \| |    ▌
                                              ▌   | (_) |\ V / | _| |   /|_|    ▌
                                              ▌    \___/  \_/  |___||_|_\(_)    ▌
                                              ▌                                 ▌
                                              ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                                                """)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__ == '__main__':
    print("Hello this is Tetris")
    tetris = Tetris()
    tetris.main()
