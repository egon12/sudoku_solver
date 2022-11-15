import numpy as np
from board import Board
from solver import Probabilities

verlin = "|"
horlin = "-"

class DualPrinter:
    def __init__(self):
        self.p1 = Printer()
        self.p2 = Printer()


    def print(self):
        for i in range(self.p1.c.shape[0]):
            line = ''
            for j in range(self.p1.c.shape[1]):
                line += self.p1.c[i, j]
            line += ' '
            for j in range(self.p1.c.shape[1]):
                line += self.p2.c[i, j]
            print(line)


class Printer:
    def __init__(self):
        self.c = np.empty((37,37), dtype=str)
        self.c[:] = " "
        self.c[:,0::4] = verlin
        self.c[::4,:] = "-"


    def _board_addr(self, row, col):
        return row*4 + 2, col*4 + 2

    def _fill_num(self, row, col, num):
        if num == 0:
            self.c[self._board_addr(row, col)] = ' '
            return
        self.c[self._board_addr(row, col)] = str(num)

    def _fill_prob(self, row, col, prob):
        row, col = self._board_addr(row, col)
        if 1 in prob:
            self.c[row-1, col-1] = '1'
        if 2 in prob:
            self.c[row-1, col  ] = '2'
        if 3 in prob:
            self.c[row-1, col+1] = '3'


        if 4 in prob:
            self.c[row, col-1] = '4'
        if 5 in prob:
            self.c[row, col  ] = '5'
        if 6 in prob:
            self.c[row, col+1] = '6'

        if 7 in prob:
            self.c[row+1, col-1] = '7'
        if 8 in prob:
            self.c[row+1, col  ] = '8'
        if 9 in prob:
            self.c[row+1, col+1] = '9'

    def fill(self, board: Board):
        for row in range(9):
            for col in range(9):
                self._fill_num(row, col, board.board[row, col])

    def fill_prob(self, prob: Probabilities):
        for row in range(9) :
            for col in range(9):
                self._fill_prob(row, col, prob[row, col])

    def print(self):
        for i in self.c:
            line = ''
            for j in i:
                line += j 
            print(line)


if __name__ == "__main__":
    p = Printer()
    p._fill_num(0,0,1)

    board = Board()
    board.fill([
        [1,2,3,4,5,6,7,8,9],
        [4,5,6,7,8,9,1,2,3],
        [7,8,9,1,2,3,4,5,6],

        [2,3,4,5,6,7,8,9,1],
        [5,6,7,8,9,1,2,3,4],
        [8,9,1,2,3,4,5,6,7],

        [3,4,5,6,7,8,9,1,2],
        [6,7,8,9,1,2,3,4,5],
        [9,1,2,3,4,5,0,0,0],
        ])

    p.fill(board)
    p.print()

    prob = Probabilities()
    p.fill_prob(prob)
    p.print()
    
