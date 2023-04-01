import unittest
from killer_adv import Solver, BoardGroup
from solver import Probabilities

class TestSolver(unittest.TestCase):

    def test_solver(self):
        bg = BoardGroup.read_from_file('killer_input.txt')
        print(bg)
        solver = Solver()
        solver.solve(bg)

        p = Probabilities()


        #self.assertTrue(s.board.is_valid())


if __name__ == '__main__':
    unittest.main()


