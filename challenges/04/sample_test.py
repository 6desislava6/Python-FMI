import unittest
import os
import solution
import shutil


CLASSES_FILE = """
class A:
    def pleasent_func(self, a, b):
        return a + b
    def a_unpleasant_func(self, a, b):
        for x in range(a):
            for y in range(b):
                if x + y > b-a:
                    return x + y
class B:
    def pleasant_func(self, a, b):
        if a + b > 0:
            return a + b
    def b_unpleasant_func(self, a, b):
        try:
            result = set()
            for x in range(a):
                for y in range(b):
                    if x + y == 0:
                        result.append(x/y)
        except ZeroDivisionError as e:
            print(e)
class C:
    pass
class D:
    pass
"""


FUNCTION_FILE = """
def unpleasant_func(a, b):
    result = []
    for x in range(a):
        for y in range(b):
            if x+y > 0:
                result.append(x+y)
def a_very_unpleasant_func(a, b, path_to_file):
    try:
        for x in range(a):
            for y in range(b):
                if x/y == 10:
                    with open(path_to_file, 'w') as f:
                        f.write(a+b)
    except ZeroDivisionError as e:
        print(e)
def pleasant_func(a, b, path_to_file):
    try:
        d = a/b
        with open(path_to_file) as f:
            buf = f.readlines()
        while d > 0:
            d -= 1
    except ZeroDivisionError as e:
        print(e)
def sum(a, b):
    while a + b > 0:
        for x in range(a):
            for y in range(b):
                a -= 1
    return a + b
"""


class TestAst(unittest.TestCase):
    def setUp(self):
        self.path = "testcode"
        self.function_dir = "testcode/functions"
        self.classes_dir = "testcode/classes"
        self.functions_file = "testcode/functions/functions.py"
        self.classes_file = "testcode/classes/classes.py"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.function_dir):
            os.makedirs(self.function_dir)
        if not os.path.exists(self.classes_dir):
            os.makedirs(self.classes_dir)
        with open(self.functions_file, 'w') as functions:
            functions.write(FUNCTION_FILE)
        with open(self.classes_file, 'w') as functions:
            functions.write(CLASSES_FILE)

    def tearDown(self):
        shutil.rmtree(self.path)

    def testStats(self):
        unpleasant = [self.classes_file + '#a_unpleasant_func',
                      self.classes_file + '#b_unpleasant_func',
                      self.functions_file + '#unpleasant_func',
                      self.functions_file + '#a_very_unpleasant_func',
                      self.functions_file + '#sum'
                      ]

        excpected = {'classes': 4,
                     'functions': 8,
                     'unpleasant_functions': unpleasant}
        result = solution.stats(self.path)
        self.assertEqual(result['classes'], excpected['classes'])
        self.assertEqual(result['functions'], excpected['functions'])

        for function in excpected['unpleasant_functions']:
            self.assertIn(function, result['unpleasant_functions'])
        for function in result['unpleasant_functions']:
            self.assertIn(function, excpected['unpleasant_functions'])

        with self.assertRaises(NotADirectoryError):
            solution.stats('wrongPathToDirectory')


if __name__ == "__main__":
    unittest.main()
