import unittest
from board import Board, Validation

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_col_row_box(self):
        self.board.fill([
            [1,2,3,4,5,6,7,8,9],
            [4,5,6,7,8,9,1,2,3],
            [7,8,9,1,2,3,4,5,6],

            [2,3,4,5,6,7,8,9,1],
            [5,6,7,8,9,1,2,3,4],
            [8,9,1,2,3,4,5,6,7],

            [3,4,5,6,7,8,9,1,2],
            [6,7,8,9,1,2,3,4,5],
            [9,1,2,3,4,5,6,7,8],
            ])
        self.assertEqual(self.board.row(0).tolist(), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(self.board.col(0).tolist(), [1, 4, 7, 2, 5, 8, 3, 6, 9])
        self.assertEqual(self.board.box(0,0).tolist(), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_board_is_valid(self):
        self.board.fill([
            [1,2,3,4,5,6,7,8,1],
            [4,5,6,7,8,9,1,2,3],
            [7,8,9,1,2,3,4,5,6],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            ])
        self.assertEqual(self.board.is_valid(), Validation(False, "Row 1 has duplicate value 1 at col 1 and 9"))

        self.board.fill([
            [1,2,3,4,5,6,7,8,9],
            [4,5,6,7,8,9,1,2,3],
            [7,8,1,0,2,3,4,5,6],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            ])
        self.assertEqual(self.board.is_valid(), Validation(False, "Box 0, 0 has duplicate value 1"))

    def test_board_equal(self):
        board1 = Board()
        board1.fill([
            [1,2,3,4,5,6,7,8,1],
            [4,5,6,7,8,9,1,2,3],
            [7,8,9,1,2,3,4,5,6],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            ])

        board2 = Board()
        board2.fill([
            [1,2,3,4,5,6,7,8,1],
            [4,5,6,7,8,9,1,2,3],
            [7,8,9,1,2,3,4,5,6],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            ])

        self.assertEqual(board1, board2)


if __name__ == '__main__':
    unittest.main()
