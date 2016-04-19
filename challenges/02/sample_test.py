import unittest

import solution


class TestImages(unittest.TestCase):
    image = [
        [(0, 0, 255), (0, 255, 0), (0, 0, 255)],
        [(255, 0, 0), (0, 0, 255), (0, 255, 0)],
        [(0, 255, 0), (0, 255, 0), (255, 0, 0)]]

    def test_grayscale_rotate_left(self):
        rotated = solution.rotate_left(self.image)
        expected = [
            [tuple([85 for i in range(3)]) for i in range(3)]
            for i in range(3)]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                self.assertEqual(expected[i][j], rotated[i][j])

    def test_grayscale_lighten(self):
        lighten = solution.lighten(self.image, 0.5)
        expected = [
            [tuple([170 for i in range(3)]) for i in range(3)]
            for i in range(3)]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                self.assertEqual(expected[i][j], lighten[i][j])

    def test_grayscale_invert(self):
        inverted = solution.invert(self.image)
        expected = [
            [tuple([170 for i in range(3)]) for i in range(3)]
            for i in range(3)]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                self.assertEqual(expected[i][j], inverted[i][j])

    def test_grayscale_darken(self):
        inverted = solution.darken(self.image, 0.5)
        expected = [
            [tuple([42 for i in range(3)]) for i in range(3)]
            for i in range(3)]

        for i in range(len(expected)):
            for j in range(len(expected[0])):
                self.assertEqual(expected[i][j], inverted[i][j])


if __name__ == '__main__':
    unittest.main()
