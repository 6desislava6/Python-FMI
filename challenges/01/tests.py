import unittest
from bodyMassIndex import shape_of


class TestBodyMassIndex(unittest.TestCase):

    def test_shape_of(self):
        self.assertEqual(shape_of(14, 1), 'тежко недохранване')
        self.assertEqual(shape_of(15, 1), 'тежко недохранване')
        self.assertEqual(shape_of(15.1, 1), 'средно недохранване')
        self.assertEqual(shape_of(16, 1), 'средно недохранване')
        self.assertEqual(shape_of(16.1, 1), 'леко недохранване')
        self.assertEqual(shape_of(18.5, 1), 'леко недохранване')
        self.assertEqual(shape_of(18.6, 1), 'нормално тегло')
        self.assertEqual(shape_of(25, 1), 'нормално тегло')
        self.assertEqual(shape_of(25.1, 1), 'наднормено тегло')
        self.assertEqual(shape_of(30, 1), 'наднормено тегло')
        self.assertEqual(shape_of(30.1, 1), 'затлъстяване I степен')
        self.assertEqual(shape_of(35, 1), 'затлъстяване I степен')
        self.assertEqual(shape_of(35.1, 1), 'затлъстяване II степен')
        self.assertEqual(shape_of(40, 1), 'затлъстяване II степен')
        self.assertEqual(shape_of(42, 1), 'затлъстяване III степен')
        self.assertEqual(shape_of(442, 1), 'затлъстяване III степен')

        self.assertEqual(shape_of(55, 1.65), 'нормално тегло')
        self.assertEqual(shape_of(14 * 1.7 ** 2, 1.7), 'тежко недохранване')
        self.assertEqual(shape_of(15 * 1.7 ** 2, 1.7), 'тежко недохранване')
        self.assertEqual(shape_of(15.1 * 1.7 ** 2, 1.7), 'средно недохранване')
        self.assertEqual(shape_of(16 * 1.7 ** 2, 1.7), 'средно недохранване')
        self.assertEqual(shape_of(16.1 * 1.7 ** 2, 1.7), 'леко недохранване')
        self.assertEqual(shape_of(18.5 * 1.7 ** 2, 1.7), 'леко недохранване')
        self.assertEqual(shape_of(18.6 * 1.7 ** 2, 1.7), 'нормално тегло')
        self.assertEqual(shape_of(25 * 1.7 ** 2, 1.7), 'нормално тегло')
        self.assertEqual(shape_of(25.1 * 1.7 ** 2, 1.7), 'наднормено тегло')
        self.assertEqual(shape_of(30 * 1.7 ** 2, 1.7), 'наднормено тегло')
        self.assertEqual(
            shape_of(30.1 * 1.7 ** 2, 1.7), 'затлъстяване I степен')
        self.assertEqual(shape_of(35 * 2**2, 2), 'затлъстяване I степен')
        self.assertEqual(shape_of(35.1 * 2**2, 2), 'затлъстяване II степен')
        self.assertEqual(shape_of(40 * 2**2, 2), 'затлъстяване II степен')
        self.assertEqual(shape_of(42 * 2**2, 2), 'затлъстяване III степен')
        self.assertEqual(shape_of(442 * 2**2, 2), 'затлъстяване III степен')


if __name__ == '__main__':
    unittest.main()
