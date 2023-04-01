import numpy as np

class Solver:
    def __init__(self, board):
        self.board = board
        self.prob = Probabilities()
        self.board_history = []
        self.board_history_message = []
        self.prob_history = []
        self.prob_history_message = []
        self.update_prob()

    def solve(self):
        for i in range(10000):
            if not self.step():
                break

    def step(self):
        self.save_prob("step")
        self.minimize_prob()
        self.get_unique_probability()
        self.fill_if_possible()

        if self.board.is_finish():
            print("Finish!!!")
            return False

        if not self.board.is_valid():
            print("Invalid value for board")
            print(self.board.is_valid())
            return False

        if self.prob == self.prob_history[-1]:
            self.save_prob("prob are same?")
            print("prob are same")
            return False

        return True

    def update_prob(self):
        """
            update the probability table if
            there are already value in board
        """
        for pos in self.board.all_filled_cell():
            if not self.prob.got_value(pos):
                self.prob[pos] = self.board[pos]
                self.save_prob("{} update from board".format(pos))


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
            removed = False

            for i in self.board.siblings(pos):
                if i != 0 and i in self.prob[pos]:
                    self.prob.remove(pos, i)
                    removed = True

            if removed:
                self.save_prob("{} minimize".format(pos))

    def get_unique_probability(self):
        for pos in self.board.all_empty_cell():
            y, x = pos
            have = self.prob[pos]
            avail = self.prob.row(pos)
            self.set_unique_prob(pos, have, avail, x, "row")

            have = self.prob[pos]
            avail = self.prob.col(pos)
            self.set_unique_prob(pos, have, avail, y, "col")

            have = self.prob[pos]
            avail = self.prob.box(pos)
            self.set_unique_prob(pos, have, avail, (y%3) * 3 + (x%3), "box")

    def set_unique_prob(self, pos, have, avail, index_in_avail, type):
        if len(have) == 1:
            return

        for i in have:
            c = str(i)

            found = 0
            for j in range(len(avail)):
                if j == index_in_avail:
                    continue
                
                if c in avail[j]:
                    found += 1

            if found == 0:
                self.save_prob("{}, unique {}, {}, {}, {}".format(pos, type, have, index_in_avail, avail))
                self.prob[pos] = i
                return

    def save_prob(self, message):
        self.prob_history.append(self.prob.clone())
        self.prob_history_message.append(message)

    def fill_if_possible(self):
        filled = False

        for pos in self.board.all_empty_cell():
            if val := self.prob.got_value(pos):
                self.board[pos] = val
                filled = True
                if not (valid := self.board.is_valid()):
                    raise Exception(str(valid))

        if filled:
            self.board_history.append(self.board.clone())
            self.board_history_message.append("filled at {}".format(len(self.prob_history)))
            self.update_prob()
                
    #def get_best_options(self):

    #def get_cells_with_num_options(self, num):
    #    for y in range(9):
    #        for x in range(9):
    #    

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
        self.arr[key] = str(val)

    def __delitem__(self, key, val):
        self.arr[key] = ""

    def __eq__(self, other):
        return np.array_equal(self.arr, other.arr)

    def __ne__(self, other):
        return not self.__eq__(other)


    def clone(self):
        p = Probabilities()
        p.arr = self.arr.copy()
        return p

    def remove(self, key, val):
        self.arr[key] = self.arr[key].replace(str(val), "")

    def set(self, key, val):
        val.sort()
        self.arr[key] = ''.join(map(lambda v: str(v), val))

    def col(self, pos):
        return self.arr[:, pos[1]]

    def row(self, pos):
        return self.arr[pos[0], :]

    def box(self, pos):
        row, col = pos
        row, col = row // 3, col // 3
        return self.arr[row*3:row*3+3, col*3:col*3+3].reshape(1,9)[0]

    def got_value(self, pos):
        if len(self.arr[pos]) == 1:
            return self.arr[pos][0]
        return False


