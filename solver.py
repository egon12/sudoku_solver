import numpy as np

class Probabilities:
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

    def col(self, col):
        return self.arr[:, col]

    def row(self, row):
        return self.arr[row, :]

    def box(self, row, col):
        row, col = row // 3, col // 3
        return self.arr[row*3:row*3+3, col*3:col*3+3].reshape(1,9)[0]



class Solver:
    def __init__(self, board):
        self.board = board
        self.prob = Probabilities()
        self.board_history = []
        self.prob_history = []
        self.prob_history_message = []
        self.update_prob()

    def save_prob(self, message):
        self.prob_history.append(self.prob.clone())
        self.prob_history_message.append(message)


    def solve(self):
        for i in range(10000):
            if not self.step():
                break

    def step(self):
        self.board_history.append(self.board.clone())
        self.save_prob("step")
        self.minimizeProbabilities()
        self.getUniqueProbabilities()
        self.fill_if_possible()
        self.update_prob()

        if self.prob == self.prob_history[-1]:
            print("prob are same")
            return False

        if not self.board.is_valid():
            print(self.board.is_valid())
            print("board not valid")
            return False

        if self.board.is_finish():
            print("board are finish")
            return False

        return True

    def update_prob(self):
        for y in range(9):
            for x in range(9):
                i = self.board[y, x]
                if i != 0 and len(self.prob[y,x]) > 1:
                    self.prob[y, x] = i
                    self.save_prob("{} update".format((x,y)))



    def minimizeProbabilities(self):
        for y in range(9):
            for x in range(9):
                if self.board[y, x] == 0:
                    self.minimizeProbabilitiesForCell(x, y)

    def getUniqueProbabilities(self):
        for y in range(9):
            for x in range(9):
                if self.board[y, x] == 0:
                    self.getUnique(x, y)


    def getUnique(self, x, y):
        have = self.prob[y, x]
        avail = self.prob.row(y)
        self.set_unique_prob(x, y, have, avail, x, "row")

        have = self.prob[y, x]
        avail = self.prob.col(x)
        self.set_unique_prob(x, y, have, avail, y, "col")

        have = self.prob[y, x]
        avail = self.prob.box(y, x)
        self.set_unique_prob(x, y, have, avail, (y%3) * 3 + (x%3), "box")



    def set_unique_prob(self, x, y, have, avail, index_in_avail, type):
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
                self.save_prob("{}, unique {}, {}, {}, {}".format((x,y), type, have, index_in_avail, avail))
                self.prob[y, x] = i
                return


    def minimizeProbabilitiesForCell(self, x, y):
        b = self.board
        avail = list(b.row(y)) + list(b.col(x)) + list(b.box(y, x))
        avail = list(set(avail))
        for i in avail:
            if i != 0 and len(self.prob[y, x]) > 1:
                self.prob.remove((y, x), i)
                self.save_prob("{}, minimize".format((x,y)))


    def fill_if_possible(self):
        for y in range(9):
            for x in range(9):
                if self.board[y, x] == 0:
                    if len(self.prob[y, x]) == 1:
                        self.board[y, x] = self.prob[y, x][0]
                        val =self.board.is_valid()
                        if not val:
                            raise Exception(val.__str__())

