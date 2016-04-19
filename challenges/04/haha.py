import ast
import inspect


class One:
    def b(self):
        while 1:
            if 6:
                return 6
        if 1:
            if 1:
                if 1:
                    return 1

# + 2 заради Module, Function


def b(self):
        while 1:
            if 6:
                return 6
        if 1:
            if 1:
                if 1:
                    return 1


def unpleasant_one():
    for x in ["smiling", "girl"]:
        for y in ["cool", "long beard", "boy"]:
            if x == 'girl' and y == 'long beard':
                print("А {} {}!".format(y, x))
