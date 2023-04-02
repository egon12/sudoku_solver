import numpy as np
from board import Board, Validation

class Option:
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value

    def __str__(self):
        return "{}: {}".format(self.pos, self.value)

class Finish():
    def __bool__(self):
        return False

class Invalid(BaseException):
    def __init__(self, validation: Validation):
        self.validation = validation

    def __bool__(self):
        return False

class Stuck:
    def __init__(self, board: Board, board_index:int = 0, prob_index:int = 0):
        self.board = board
        self.board_index = board_index

    def __bool__(self):
        return False

    def __repr__(self):
        return str(self.board.board)

class Solver:
    def __init__(self, board):
        self.board = board
        self.prob = Probabilities()
        self.board_history = []
        self.board_history_message = []
        self.prob_history = []
        self.prob_history_message = []

        self.save_board("start")
        self.save_prob("start")

        self.update_prob()

    def solve(self):
        for i in range(10000):
            if not (condition := self.step()):
                return condition
                

    def step(self):
        try:
            self.minimize_prob()
            self.fill_minimized()
            self.fill_unique()

            if self.board.is_finish():
                return Finish()

            if not (validation := self.board.is_valid()):
                return Invalid(validation)

            if self.prob == self.prob_history[-1]:
                return Stuck(self.board.clone(), len(self.board_history) -1)

        except Invalid as e:
            return e

        return True

    def update_prob(self):
        """
            update the probability table if
            there are already value in board
        """
        filled_pos = []
        for pos in self.board.all_filled_cell():
            if not self.prob.got_value(pos):
                self.prob[pos] = self.board[pos]
                filled_pos.append(pos)

        self.save_prob("copy from real value for {}".format(filled_pos))

    def minimize_prob(self):
        """
            First minimize_prob will check the cell is empty.
            If it is empty, it will check the siblings of the cell.
            If the siblings has value, it will remove the value from the cell's probability

            The siblings are set from 3 group.
            1. row's siblings
            2. columns's siblings
            3. box's siblings
        """
        for pos in self.board.all_empty_cell():
            removed = []

            for i in self.board.siblings(pos):
                if i != 0 and i in self.prob[pos]:
                    del self.prob[pos, i]
                    removed.append(i)

            if len(removed) > 0:
                self.save_prob("{} is removed from {}".format(removed, pos))

    def fill_unique(self):
        """
            find unique value within it's group (row, col and box)
            and if found, set the value in real and prob
        """
        for pos in self.board.all_empty_cell():
            if val := Unique.find(self.prob, pos):
                num, group = val
                self.save_prob("set {} as unique val within {} in {}".format(num, group, pos))
                self.prob[pos] = num 
                self.board[pos] = num
                self.save_board()


    def fill_minimized(self):
        """
            fill empty cell with prob that only got 1 value
        """
        filled = False

        for pos in self.board.all_empty_cell():
            if val := self.prob.got_value(pos):
                self.board[pos] = val
                filled = True

        if filled:
            self.save_board()
            self.update_prob()

    def save_prob(self, message):
        self.prob_history.append(self.prob.clone())
        self.prob_history_message.append(message)

    def save_board(self, message=""):
        self.board_history.append(self.board.clone())
        self.board_history_message.append("filled at {}".format(len(self.prob_history)))
                
    def get_best_options(self):
        pos, prob = self.prob.smallest_probability()
        return list(map(lambda val: Option(pos, int(val)), prob))

    def follow_option(self, option: Option):
        self.board[option.pos] = option.value
        self.prob[option.pos] = option.value
        self.save_prob("choose option {}".format(option))
        self.save_board()
        return self.solve()

    def back_to(self, stuck: Stuck):
        self.board = stuck.board.clone()
        self.prob = Probabilities()
        self.update_prob()

class Probabilities:
    """
    9x9 array of probabilities
    """
    def __init__(self):
        p = "123456789"
        p = np.array([p,p,p,p,p,p,p,p,p])
        p = np.array([p,p,p,p,p,p,p,p,p])
        self.arr = p

    def __getitem__(self, key):
        res = []
        for c in self.arr[key]:
            res.append(int(c))
        return res

    def __setitem__(self, key, val):
        if isinstance(val, list):
            val.sort()
            self.arr[key] = ''.join(map(lambda v: str(v), val))
        elif isinstance(val, int):
            self.arr[key] = str(val)
        elif isinstance(val, np.int8):
            self.arr[key] = str(val)
        else:
            raise Exception("cannot set prob with {}".format(type(val)))
        
    def __delitem__(self, key):
        if not isinstance(key, tuple):
            raise Exception("Need pos to delete probability")

        if len(key) != 2:
            raise Exception("Need pos(row,col) to delete probability")

        if isinstance(key[0], tuple):
            val = key[1]
            key = key[0]
            self.arr[key] = self.arr[key].replace(str(val), "")
            return

        self.arr[key] = ""

    def __eq__(self, other):
        return np.array_equal(self.arr, other.arr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def clone(self):
        p = Probabilities()
        p.arr = self.arr.copy()
        return p

    def row(self, pos):
        return self.arr[pos[0], :]

    def col(self, pos):
        return self.arr[:, pos[1]]

    def box(self, pos):
        row, col = pos

        r_start = (row // 3) * 3
        c_start = (col // 3) * 3

        r_end = r_start + 3
        c_end = c_start + 3

        return self.arr[r_start:r_end, c_start:c_end].reshape(1,9)[0]

    def got_value(self, pos):
        if len(self.arr[pos]) == 1:
            return int(self.arr[pos][0])
        return False

    def smallest_probability(self):
        for num in range(2, 10):
            if got := self.get_pos_with_number(num):
                return got
        raise Exception("Probability table is broken")


    def get_pos_with_number(self, num):
        for row in range(9):
            for col in range(9):
                pos = (row, col)
                pro = self.arr[pos]
                if len(pro) == num:
                    return pos, pro
        return False
                    
class Unique:
    def find(prob, pos):
        if num := Unique.find_in(prob.row, prob, pos):
            return num, 'row'

        if num := Unique.find_in(prob.col, prob, pos):
            return num, 'col'

        if num := Unique.find_in(prob.box, prob, pos):
            return num, 'box'

        return False

    def find_in(groups, prob, pos):
        # all probs that will be evaluated
        all_probs = list(groups(pos)) # ['1234', '1235', '1278'....]

        # TODO need to check another way to ge the strings
        pos_prob = prob.arr[pos] # '1235'

        # remove the pos_probe so in the pos_prob can be unique
        # ex: ['123', '1459', '145', '178'].remove('1459') so we can 9 as unique number
        all_probs.remove(pos_prob)

        all_number = ''.join(all_probs)
        unique_number = list(set(all_number))
        unique_siblings = list(map(int, unique_number)) # {1,2,3,4,7,8}

        # set group_probs[index] to empty so it wouldn't affect the unique
        for p in prob[pos]:
            if p not in unique_siblings:
                return p

        return False

class Backtrack:
    def __init__(self, solver):
        self.solver = solver
        self.condition = []
        self.memory = {}

    def walk(self):
        cond = self.solver.solve()
        fin = self.rec_walk(cond)
        return next(fin)

    def rec_walk(self, cond):
        if isinstance(cond, Invalid):
            return cond

        if isinstance(cond, Finish):
            yield cond

        if isinstance(cond, Stuck):
            for idx, opt in enumerate(self.solver.get_best_options()):
                self.solver.back_to(cond)
                new_cond = self.solver.follow_option(opt)
                yield from self.rec_walk(new_cond)

        raise Exception("Deadend")
