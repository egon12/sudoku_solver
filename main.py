from solver import Solver, Probabilities
from printer import Printer, DualPrinter
from killer_adv import BoardGroup
from killer_adv import Solver as KillerSolver
from board import Board

def main():

    bg = BoardGroup.read_from_file('killer_input4.txt')

    b = Board()
    b.fill([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],

        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 0],

        ])
    prob = Probabilities()

    ks = KillerSolver()

    for group in bg.groups:
        probabilities = ks.possibilities_cell(group)
        for cell in group.cells:
            position = group.pos(cell)
            prob[position] = probabilities

    s = Solver(b)
    s.prob = prob

    for i in range(100):
        kill_step(bg, ks, s.board, s.prob)
        s.step()
        pall(s.board, s.prob)
        input("Press Enter to continue...")


def pall(board: Board, prob: Probabilities):
    p = DualPrinter()
    p.p1.fill(board)
    p.p2.fill_prob(prob)
    p.print()

def kill_step(bg: BoardGroup, ks: KillerSolver, board: Board, prob: Probabilities):
    for g in bg.groups:
        includes = []
        excludes = []
        for c in g.cells:
            f = board[g.pos(c)]
            if f != 0:
                includes.append(f)

        if g.is_one_row():
            excludes += board.row(g.first_pos()).tolist()

        if g.is_one_col():
            excludes += board.col(g.first_pos()).tolist()

        if g.is_one_box():
            excludes += board.box(g.first_pos()).tolist()

        for i in includes:
            if i in excludes:
                excludes.remove(i)

        som = ks.possibilities_cell(g, include=includes, exclude=excludes)
        for c in g.cells:
            x, y = getxy(c)
            prob[y, x] = som


def getxy(c):
    y = (c // 10) - 1
    x = (c % 10) - 1
    return (x, y)

if __name__ == "__main__":
    main()

