from solver import Solver, Backtrack
from input import FileInput, ImageInput
from printer import DualPrinter, Printer
from killer_adv import BoardGroup
from killer_adv import Solver as KillerSolver
from board import Board

import termios

# Get the current attributes of the terminal
attrs = termios.tcgetattr(0)

# Disable ICANON mode
attrs[3] &= ~termios.ICANON

# Set the new attributes for the terminal
termios.tcsetattr(0, termios.TCSANOW, attrs)

def main():
    b = ImageInput("screen_1.png").read()
    s = Solver(b)
    w = Backtrack(s)

    try: 
        c = w.walk()
    except Exception as e:
        print(e)

    while(True):
        interact(s)


def interact(s):
    l = len(s.prob_history)
    i = l - 1

    k = len(s.board_history)
    j = k - 1


    while (True):
        c = input()
        if c == "q":
            exit(0)
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
        elif c == "c":
            cont(s)
            break

        # go to origin
        print('\033[1;1H')
        # clear the screen
        print('\033[2J')
        print_solver(s, i, j)


def print_solver(s, i, j):
    print("probs {}: {}".format(i, s.prob_history_message[i]))
    print("board: {}: {}".format(j, s.board_history_message[j]))
    p = DualPrinter()
    p.p2.fill_prob(s.prob_history[i])
    p.p1.fill(s.board_history[j])
    p.print()

def cont(s):
    opts = s.get_best_options()
    print(opts)
    print("choose")
    print(opts[1])
    cond = s.follow_option(opts[1])
    print(cond)



if __name__ == "__main__":
    main()

