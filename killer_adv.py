
class Group:
    def __init__(self, sum, cells):
        self.sum = sum
        self.cells = cells

    def key(self):
        return (self.sum, len(self.cells))

    def __str__(self):
        return str(self.sum) + ':' + str(self.cells)

    def __repr__(self):
        return str(self.sum) + ':' + str(self.cells)

    def pos(self, cell):
        return (cell // 10) - 1, (cell % 10) - 1

    def is_one_row(self):
        x = set(map(lambda c: self.pos(c)[0], self.cells))
        return len(x) == 1

    def is_one_col(self):
        y = set(map(lambda c: self.pos(c)[1], self.cells))
        return len(y) == 1

    def is_one_box(self):
        y = set(map(lambda c: _get_box_id(self.pos(c)), self.cells))
        return len(y) == 1

    def row(self):
        return self.pos(self.cells[0])[0]
    
    def col(self):
        return self.pos(self.cells[0])[1]

    def box(self):
        return self.pos(self.cells[0])

    def first_pos(self):
        return self.pos(self.cells[0])


class BoardGroup:
    def __init__(self, groups):
        self.groups = groups
        self.check()

    def check(self):
        s = sum(map(lambda g: g.sum, self.groups))
        if s != 405:
            raise Exception('sum of groups is not 405')

        ucl = list(map(lambda g: g.cells, self.groups))
        uc = sum(ucl, [])

        for y in range(1, 10):
            for x in range(1, 10):
                c = y * 10 + x
                if c not in uc:
                    raise Exception('num ' + str(c) + ' is not exists')
                    #raise Exception('num ' + str(c) + ' is not exists in ' + str(uc))
        

    def read_from_file(file):
        f = open(file)
        s = f.read()
        f.close()

        r = s.split('\n')

        row = []
        for rr in r:
            tmp = rr.split(':')
            if len(tmp) > 1:
                row.append(tmp)


        groups = list(map(lambda r: Group(int(r[0]), toset(r)), row))

        return BoardGroup(groups)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        res = ""
        for g in self.groups:
            res += str(g) + '\n'
        return res

class Solver:
    def __init__(self):
        self.allpos = genmap()

    def possibilities(self, g, include=[], exclude=[]):
        k = g.key()
        p = self.allpos[k]

        p = filter(lambda i: self._is_exclude(i, exclude), p)
        p = filter(lambda i: self._is_include(i, include), p)
        return list(p)

    def possibilities_cell(self, g, include=[], exclude=[]):
        p = self.possibilities(g, include, exclude)
        res = []
        for i in p:
            res += i
        return list(set(res))


    def _is_exclude(self, posibilities, exclude):
        for e in exclude:
            if e in posibilities:
                return False
        return True

    def _is_include(self, posibilities, include):
        for i in include:
            if i not in posibilities:
                return False
        return True

def genadd(prev, num, digits):
    if num == 0:
        yield digits
        return

    for i in range(prev+1, 10):
        d = digits.copy()
        d.append(i)
        yield from genadd(i, num - 1, d)

def genmap():
    res = []
    for i in range(1, 10):
        res += list(genadd(0,i,[]))

    d = {}

    for i in res:
        s = sum(i)
        l = len(i)
        k = (s,l)
        if k not in d:
            d[k] = []
        d[k].append(i)
    return d


def toset(c):
    res = []
    for cn in c[1].split(' '):
        try:
            res.append(int(cn))
        except:
            continue
    return res


def _get_box_id(key):
    (row, col) = key
    return row // 3, col // 3

if __name__ == '__main__':
    bg = BoardGroup.read_from_file('input.txt')

    s = Solver()

    for g in bg.groups:
        print(s.possibilities(g))



