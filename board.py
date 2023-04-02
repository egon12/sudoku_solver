import numpy as np

class Board:
    """
    class Board contains the real value of the sudoku cell.

    to access the cell you must use the following syntax:

        board[row, col] = value
        board[row, col] = 0

    and to get the value of the cell:
        
        value = board[row, col]

    """
    def __init__(self):
        self.board = np.zeros((9,9), dtype=np.int8)

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        if self.board[key] != 0:
            print(self.board)
            raise Exception("Cell {} is already filled".format(key))
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

    def col(self, pos):
        return self.board[:, pos[1]]

    def row(self, pos):
        return self.board[pos[0], :]

    def box(self, pos):
        row, col = pos
        row, col = row // 3, col // 3
        return self.board[row*3:row*3+3, col*3:col*3+3].reshape(1,9)[0]

    def is_finish(self):
        if self.is_valid():
            return not (self.board == 0).any()
        return False

    def is_valid(self):
        return Validator.validate_board(self)

    def is_empty(self, key):
        return self.board[key] == 0

    def siblings(self, pos):
        avail = list(self.row(pos)) + list(self.col(pos)) + list(self.box(pos))
        return list(set(avail))

    def all_cell(self):
        for row in range(9):
            for col in range(9):
                yield(row, col)

    def all_empty_cell(self):
        return filter(self.is_empty, self.all_cell())

    def all_filled_cell(self):
        return filter(lambda c: not self.is_empty(c), self.all_cell())

class Validator:
    def validate_board(board: Board):
        for row in range(9):
            for col in range(9):
                pos = (row, col)
                if not (validation := Validator.validate_cell(board, pos)):
                    return validation
        return Valid()

    def validate_cell(board, pos):
        if board[pos] == 0:
            return Valid()

        val = board[pos]

        row, col = pos

        arr = board.row(pos)
        for i in range(9):
            if i != col and arr[i] == val:
                return Invalid("Row {} has duplicate value {} at col {} and {}".format(row + 1, val, col + 1, i + 1))

        arr = board.col(pos)
        for i in range(9):
            if i != row and arr[i] == val:
                return Invalid("Col {} has duplicate value {} at row {} and {}".format(col + 1, val, row + 1, i + 1))

        arr = board.box((row, col))
        dup = False
        for i in arr:
            if i == val:
                if dup:
                    return Invalid("Box ({},{}) has duplicate value {}".format(col, row, val))
                else:
                    dup = True

        return Valid()

class Validation:
    def __init__(self, is_valid, error_message):
        self.is_valid = is_valid
        self.error_message = error_message

    def __bool__(self):
        return self.is_valid

    def __nonzero__(self):
        return self.is_valid

    def __eq__(self, other):
        if isinstance(other, type):
            return isinstance(self, other)

        if isinstance(other, Validation):
            return self.is_valid == other.is_valid and self.error_message == other.error_message

        raise Exception("Cannot compare Invalid with {}".format(type(other)))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Validation({}, {})".format(self.is_valid, self.error_message)

    def __str__(self):
        return self.__repr__()

class Invalid(Validation):
    def __init__(self, error_message):
        super().__init__(False, error_message)

class Valid(Validation):
    def __init__(self):
        super().__init__(True, "")
