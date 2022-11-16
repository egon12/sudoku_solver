from solver import Solver
from input import FileInput, ImageInput
from printer import Printer

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

        print(i)
        print(s.prob_history_message[i])
        p = Printer()
        p.fill_prob(s.prob_history[i])
        p.print()


if __name__ == "__main__":
    main()

