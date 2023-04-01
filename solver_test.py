import unittest
from board import Board, Validation
from solver import Solver, Probabilities
from input import FileInput
from printer import Printer, DualPrinter

class TestSolver(unittest.TestCase):

    def test_solver(self):
        board = FileInput("easy.txt").read()
        s = Solver(board)

        p = DualPrinter()

        try:
            s.solve()
        except Exception as e:
            print(e)
            p.p1.fill(s.board)
            #p.p2.fill_prob(s.prob_history[-1])
            p.p2.fill_prob(s.prob)
            p.print()
            raise e
        
        #p = Printer()
        #p.fill(s.board)
        #p.print()

        p.p1.fill(s.board)
        p.p2.fill_prob(s.prob)
        print(len(s.board_history))

        p.print()

        #p = DualPrinter()
        #p.p1.fill_prob(s.prob_history[-2])
        #p.p2.fill_prob(s.prob_history[-1])
        #p.print()
        self.assertTrue(s.board.is_valid())

        board = FileInput("easy_result.txt").read()

        self.assertEqual(board, s.board)



if __name__ == '__main__':
    unittest.main()


