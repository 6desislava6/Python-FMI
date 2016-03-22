import unittest
import solution as s


class SampleTest(unittest.TestCase):
    def test_five_plus_three(self):
        plus = s.create_operator('+', lambda lhs, rhs: lhs + rhs)
        x = s.create_variable('x')
        y = s.create_variable('y')
        added_expression = s.create_expression((x, plus, y))
        self.assertEqual(added_expression.evaluate(x=5, y=3), 8)

    def test_operators(self):
        y = s.create_variable('y')
        twelve = s.create_constant(12)
        expression = y + twelve
        self.assertEqual(expression.evaluate(y=3), 15)

    def test_constant_evaluation(self):
        self.assertEqual(s.create_variable('x').evaluate(x=42), 42)
        self.assertEqual(s.create_constant(5).evaluate(), 5)

    def test_create_constant(self):
        const = s.create_constant(4.5)
        self.assertEqual(str(const), '4.5')
        self.assertEqual(const.evaluate(), 4.5)

    def test_expressions(self):
        four = s.create_constant(4)
        y = s.create_variable('y')
        f = four/2 + 3.5*(y-2)
        d = (3+1j) + y
        z = 15 - 2/four * (12 / f)
        self.assertEqual(d.evaluate(y=2), 5+1j)
        self.assertEqual(f.evaluate(y=2), 2)
        self.assertEqual(f.evaluate(y=0), -5)
        self.assertEqual(z.evaluate(y=2, x=3), 12.0)

    def test_expression_variable_names(self):
        x = s.create_variable('x')
        y = s.create_variable('y')
        z = s.create_variable('z')
        f = (z - 2 * (x + 1j)) + 3.5*(y-2)
        variables = f.variable_names
        expected = ['x', 'y', 'z']
        print(variables)
        for v in variables:
            self.assertTrue(v in expected)
        for v in expected:
            self.assertTrue(v in variables)

    def test_str_method_of_classes(self):
        four = s.create_constant(4)
        y = s.create_variable('y')
        f = four + 3.5*(y-2)
        self.assertEqual(str(four), '4')
        self.assertEqual(str(y), 'y')
        self.assertEqual(str(f), '(4 + (3.5 * (y - 2)))')

if __name__ == '__main__':
    unittest.main()

