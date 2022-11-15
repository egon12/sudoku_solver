import numpy as np

class Board:
    def __init__(self):
        self.board = np.zeros((9,9), dtype=np.int8)

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        if self.board[key] != 0:
            raise Exception("Cell is already filled")
        self.board[key] = value

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def __ne__(self, other):
        return not self.__eq__(other)

    def clone(self):
        board = Board()
        board.board = self.board.copy()
        return board

    def fill(self, arr):
        self.board = np.array(arr, dtype=np.int8).reshape(9,9)

    def col(self, col):
        return self.board[:, col]

    def row(self, row):
        return self.board[row, :]

    def box(self, row, col):
        row, col = row // 3, col // 3
        return self.board[row*3:row*3+3, col*3:col*3+3].reshape(1,9)[0]

    def is_finish(self):
        if self.is_valid():
            return not (self.board == 0).any()
        return False

    def is_valid(self):
        return Validator.validate_board(self)

class Validator:
    def validate_board(board: Board):
        for row in range(9):
            for col in range(9):
                validation = Validator.validate_cell(board, row, col)
                if not validation:
                    return validation
        return Validation(True, "")

    def validate_cell(board, row, col):
        if board[row, col] == 0:
            return Validation(True, "")

        val = board[row, col]

        arr = board.row(row)
        for i in range(9):
            if i != col and arr[i] == val:
                return Validation(False, "Row {} has duplicate value {} at col {} and {}".format(row + 1, val, col + 1, i + 1))

        arr = board.col(col)
        for i in range(9):
            if i != row and arr[i] == val:
                return Validation(False, "Col {} has duplicate value {} at row {} and {}".format(col + 1, val, row + 1, i + 1))

        arr = board.box(row, col)
        dup = False
        for i in arr:
            if i == val:
                if dup:
                    return Validation(False, "Box ({},{}) has duplicate value {}".format(col, row, val))
                else:
                    dup = True

        return Validation(True, "")



class Validation:
    def __init__(self, is_valid, error_message):
        self.is_valid = is_valid
        self.error_message = error_message

    def __bool__(self):
        return self.is_valid

    def __nonzero__(self):
        return self.is_valid

    def __eq__(self, other):
        return self.is_valid == other.is_valid and self.error_message == other.error_message

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Validation({}, {})".format(self.is_valid, self.error_message)

    def __str__(self):
        return self.__repr__()
