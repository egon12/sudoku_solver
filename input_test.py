import unittest
from input import StringInput, FileInput

class TestStringInput(unittest.TestCase):


    def test_string_input(self):
        self.assertEqual(1, 1)
        i = "5  7 1 3 \n"
        i += " 4    2  \n"
        i += "38 94    \n"
        i += " 35687 94\n"
        i += " 6145 723\n"
        i += " 79   8  \n"
        i += "7   1    \n"
        i += "   8 45 2\n"
        i += " 5     41\n"

        board1: Board = StringInput(i).read()

        board2: Board = FileInput("easy.txt").read()

        self.assertEqual(board1, board2)


if __name__ == '__main__':
    unittest.main()
