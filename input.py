import sys
from board import Board, Validation

class StringInput:

    def __init__(self, string):
        self.string = string

    def read(self):
        board = Board()
        lines = self.string.splitlines()
        if len(lines) != 9:
            raise Exception("Invalid input, must be 9 lines")
        for i in range(9):
            line = lines[i]
            if len(line) != 9:
                raise Exception("Invalid input, line {} must be 9 characters long".format(i + 1))
            for j in range(9):
                c = line[j]
                if c == ' ':
                    board.board[i, j] = 0
                else:
                    board.board[i, j] = int(c)
        return board

class FileInput:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as f:
            return StringInput(f.read()).read()
