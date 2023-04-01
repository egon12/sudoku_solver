import unittest
from board import Board, Validation
from solver import Solver, Probabilities, Unique
from input import FileInput
from printer import Printer, DualPrinter

class TestSolver(unittest.TestCase):

    def test_solver(self):
        board = FileInput("easy.txt").read()
        s = Solver(board)

        try:
            s.solve()
        except Exception as e:
            print(e)
            raise e
        
        p = DualPrinter()
        p.p1.fill(s.board)
        p.p2.fill_prob(s.prob)

        #for sss in s.prob_history_message:
        #    print(sss)
        #print(len(s.board_history))
        #p.print()

        self.assertTrue(s.board.is_valid())

        board = FileInput("easy_result.txt").read()

        self.assertEqual(board, s.board)


class TestUnique(unittest.TestCase):

    def test_find_in_1(self):
        s = Solver(Board())
        for i in range(8):
            del s.prob[(i, 5), 1]

        pos = (8,5)

        self.assertEqual(Unique.find_in(s.prob.col, s.prob, pos), 1)

    def test_find_in_2(self):
        s = Solver(Board())
        for i in range(1, 9):
            del s.prob[(4, i), 2]

        pos = (4,0)

        self.assertEqual(Unique.find_in(s.prob.row, s.prob, pos), 2)

    def test_find_in_with_false_return(self):
        s = Solver(Board())
        s.prob.arr[0] = ['2567', '59', '4', '5679', '25679', '1', '23569', '359', '8']

        self.assertFalse(Unique.find_in(s.prob.row, s.prob, (0,0)))


if __name__ == '__main__':
    unittest.main()


