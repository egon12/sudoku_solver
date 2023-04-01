import unittest

from solver import Probabilities

class TestProbabilities(unittest.TestCase):

    def test_box_1(self):

        p = Probabilities()
        p[0,0] = 1
        p[0,1] = 4
        p[0,2] = 7
        p[1,0] = 2
        p[1,1] = 5
        p[1,2] = 8
        p[2,0] = 3
        p[2,1] = 6
        p[2,2] = 9

        self.assertEqual(p.box((1,1)).tolist(), ['1','4','7','2','5','8','3','6','9'])
        #self.assertEqual(p.box(5,5), 1)

    def test_box_2(self):

        p = Probabilities()
        p[6,0] = 1
        p[6,1] = 4
        p[6,2] = 7
        p[7,0] = 2
        p[7,1] = 5
        p[7,2] = 8
        p[8,0] = 3
        p[8,1] = 6
        p[8,2] = 9

        self.assertEqual(p.box((6,1)).tolist(), ['1','4','7','2','5','8','3','6','9'])

    def test_set_prob(self):

        p = Probabilities()
        p.remove((0,3),1)

        new_prob = p[0, 3]
        self.assertEqual(new_prob, [2,3,4,5,6,7,8,9])
        self.assertTrue(2 in p[0,3])


if __name__ == '__main__':
    unittest.main()
