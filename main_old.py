from solver import Solver
from input import FileInput, ImageInput
from printer import DualPrinter, Printer
from killer_adv import BoardGroup
from killer_adv import Solver as KillerSolver
from board import Board

def main():
    board = ImageInput("screen_1.png").read()

    p = Printer()
    p.fill(board)
    p.print()

    s = Solver(board)

    try:
        s.solve()
    except Exception as e:
        print(e)

    p = Printer()
    p.fill(s.board)
    p.print()

    l = len(s.prob_history)
    i = l - 1

    k = len(s.board_history)
    j = k - 1


    while (True):
        c = input()
        if c == "q":
            break
        elif c == "t":
            n = input()
            i = int(n)
        elif c == "n":
            i = (i+1) % l
        elif c == "p":
            i = (i-1)
            if i < 0:
                i = l-1

        elif c == "j":
            j = (j+1) % k
        elif c == "k":
            j = (j-1)
            if j < 0:
                j = k-1

        print_solver(s, i, j)

def print_solver(s, i, j):
    print("probs {}: {}\nboard: {}: {}".format(i, s.prob_history_message[i], j, s.board_history_message[j]))
    p = DualPrinter()
    p.p2.fill_prob(s.prob_history[i])
    p.p1.fill(s.board_history[j])
    p.print()




if __name__ == "__main__":
    main()

