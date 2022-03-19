import random
import copy
import os


class Game2048:
    def __init__(self):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.init_val = [2, 4]
        self.DIMENSION = 4
        self.game_over = False
        self.score = 0

    @staticmethod
    def clear_screen():
        """
         This method clears the interpreter console.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_board(self):
        """
         This method prints the whole game main-board in tables.
        """
        largest = 0
        for row in range(self.DIMENSION):   # finds the largest number in the board
            for num in range(self.DIMENSION):
                if self.board[row][num] > largest:
                    largest = self.board[row][num]
        count = len(str(largest))   # every cell of the table will be equal to the size of the largest number

        self.clear_screen()
        print("=" * 20)
        for i in range(self.DIMENSION):
            print('|', end='')
            for j in range(self.DIMENSION):
                if self.board[i][j] == 0:
                    print(' ' * count + '|', end='')
                else:
                    print(' ' * (count-len(str(self.board[i][j])))+str(self.board[i][j])+'|', end='')
            print()
        print("score: " + str(self.score))
        print("=" * 20)

    def generate_random(self):
        """
         This method generates two random numbers,
        this two numbers are the coordinate of a cell.
        """
        ran_x = random.randrange(0, self.DIMENSION, 1)
        ran_y = random.randrange(0, self.DIMENSION, 1)
        if self.board[ran_x][ran_y] != 0:   # return numbers if the cell is empty
            return self.generate_random()
        else:
            return ran_x, ran_y

    def get_random_num(self):
        """
         This method chooses a random number from init_val list
        and puts it into a random coordinate generated by generate_random method.
        """
        rand_x, rand_y = self.generate_random()
        self.board[rand_x][rand_y] = random.choice(self.init_val)

    def slide_horizontally(self, row):
        """
         This method slides the elements horizontally(to the left) and can be used in go_right
        and go_left methods.

        :param row: This is the row of our main-board that we want to slide its elements
        :return: The slided version of `row`
        """
        for k in range(self.DIMENSION - 1):
            for j in range(self.DIMENSION - 1, 0, -1):
                if row[j - 1] == 0:    # slides the element if its left is 0 and then puts 0 in its previous place
                    row[j - 1] = row[j]
                    row[j] = 0
        for j in range(self.DIMENSION - 1):
            # if the right element is equal to the current element,
            # twice the value of current element and put 0 instead of previous(right) element
            if row[j] == row[j + 1]:
                row[j] *= 2
                row[j + 1] = 0
                if row == self.board[0] or row == self.board[1] or row == self.board[2] or row == self.board[3]:
                    self.score += row[j]
        for k in range(self.DIMENSION - 2):
            # slides the other elements that are left
            for j in range(self.DIMENSION - 1, 0, -1):
                if row[j - 1] == 0:
                    row[j - 1] = row[j]
                    row[j] = 0
        return row

    def slide_left(self, bord):
        """
         This method applies the slide_horizontally method to all of the main-board's rows.
        (Slides every row to left)

        :param bord: The main-board that we wants to slide it to Left
        :return: The slided version of main-board
        """
        for i in range(self.DIMENSION):
            bord[i] = self.slide_horizontally(bord[i])
        return bord

    def reverse_row(self, row):
        """
         This method takes the row list and reverses it.

        :param row: The row list that we want to reverse
        :return: Reversed list
        """
        temp_list = []
        for i in range(self.DIMENSION - 1, -1, -1):
            temp_list.append(row[i])
        return temp_list

    def slide_right(self, bord):
        """
         This method takes the main-board as input and then reverses its rows,
        slides it to left and then reverses it again.(this process slides rows to right)

        :param bord: The main-board that we wants to slide it to Right
        :return: The slided version of main-board
        """
        for i in range(self.DIMENSION):
            bord[i] = self.reverse_row(bord[i])
            bord[i] = self.slide_horizontally(bord[i])
            bord[i] = self.reverse_row(bord[i])
        return bord

    def slide_up(self, bord):
        """
         This method slides the elements to up direction.

        :param bord: The main-board that we wants to slide it to Up
        :return: The slided version of main-board
        """
        for i in range(self.DIMENSION):
            for k in range(self.DIMENSION - 1):
                for j in range(self.DIMENSION - 1, 0, -1):
                    if bord[j - 1][i] == 0:  # slides the element if its up is 0 and then puts 0 in its previous place
                        bord[j - 1][i] = bord[j][i]
                        bord[j][i] = 0
            for j in range(self.DIMENSION - 1):
                # if the down element is equal to the current element,
                # twice the value of current element and put 0 instead of previous(down) element
                if bord[j][i] == bord[j + 1][i]:
                    bord[j][i] *= 2
                    bord[j + 1][i] = 0
                    if bord == self.board:
                        self.score += bord[j][i]
            for k in range(self.DIMENSION - 2):
                # slides the other elements that are left
                for j in range(self.DIMENSION - 1, 0, -1):
                    if bord[j - 1][i] == 0:
                        bord[j - 1][i] = bord[j][i]
                        bord[j][i] = 0

    def slide_down(self, bord):
        """
         This method slides the elements to down direction.

        :param bord: The main-board that we wants to slide it to Down
        :return: The slided version of main-board
        """
        for i in range(self.DIMENSION):
            for k in range(self.DIMENSION - 1):
                for j in range(self.DIMENSION - 1):
                    if bord[j + 1][i] == 0:  # slides the element if its down is 0 and then puts 0 in its previous place
                        bord[j + 1][i] = bord[j][i]
                        bord[j][i] = 0
            for j in range(self.DIMENSION - 1, 0, -1):
                # if the up element is equal to the current element,
                # twice the value of current element and put 0 instead of previous(up) element
                if bord[j][i] == bord[j - 1][i]:
                    bord[j][i] *= 2
                    bord[j - 1][i] = 0
                    if bord == self.board:
                        self.score += bord[j][i]
            for k in range(self.DIMENSION - 2):
                # slides the other elements that are left
                for j in range(self.DIMENSION - 1):
                    if bord[j + 1][i] == 0:
                        bord[j + 1][i] = bord[j][i]
                        bord[j][i] = 0

    def check_winning(self):
        """
         This method checks every element in main-board to find 2048.
        if it finds 2048 returns true, otherwise returns false.
        """
        for row in range(4):
            for num in range(4):
                if self.board[row][num] == 2048:
                    return True
        return False

    def check_losing(self):
        """
         This method checks for all of the moves in every direction.

         :return: if any moves left returns `False` otherwise returns `True`
        """
        temp_board1 = copy.deepcopy(self.board)
        temp_board2 = copy.deepcopy(self.board)
        self.slide_up(temp_board1)
        if temp_board1 == temp_board2:
            self.slide_down(temp_board1)
            if temp_board1 == temp_board2:
                self.slide_left(temp_board1)
                if temp_board1 == temp_board2:
                    self.slide_right(temp_board1)
                    return True
        return False

    def main(self):
        """
         This method is the main loop of the game.
        """
        while not self.game_over:
            valid_input = True
            direction = input("Enter a direction(w,a,s,d) ").lower()

            # copies the board in another list to check if the direction made is available or not
            temp_board = copy.deepcopy(self.board)

            if direction == 'w':
                self.slide_up(self.board)
            elif direction == 'a':
                self.slide_left(self.board)
            elif direction == 's':
                self.slide_down(self.board)
            elif direction == 'd':
                self.slide_right(self.board)
            elif direction == 'exit':
                break
            else:
                valid_input = False

            if not valid_input:
                print("please enter a valid direction!")
            else:
                if self.board == temp_board:
                    print("try diff direction")
                else:
                    if self.check_winning():
                        self.print_board()
                        print("***you won!***")
                        input("press ENTER to exit...")
                        self.game_over = True
                    else:
                        self.get_random_num()
                        self.print_board()

                        if self.check_losing():
                            print("you lost :(")
                            input("press ENTER to exit...")
                            self.game_over = True


if __name__ == '__main__':
    game = Game2048()
    print("""
    _______________________
    |     (2048 game)     |
    -----------------------
    """)
    input("press ENTER to start...")
    game.get_random_num()
    game.get_random_num()
    game.print_board()
    game.main()
