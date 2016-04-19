import ast
import inspect
import textwrap
import os
from importlib.machinery import SourceFileLoader
import os.path
import re


def stats(path_to_directory):
    data = {
        'classes': 0,
        'functions': 0,
        'unpleasant_functions': []
    }

    if not os.path.exists(path_to_directory):
        raise NotADirectoryError

    modules = find_modules(path_to_directory)
    for mod in modules:
        name = re.match('.*/(.*)\.py$', mod).groups()[0]
        foo = SourceFileLoader(name, mod).load_module()
        Crawler.make_all(foo, data, mod)
    return data


def find_modules(path_to_directory):
    modules = []
    for dirpath, dirnames, filenames in os.walk(path_to_directory):
        for filename in [f for f in filenames if f.endswith(".py")]:
            modules.append(os.path.join(dirpath, filename))
    return modules


class Crawler:
    GATES = [ast.If, ast.While, ast.For, ast.With,
             ast.Try, ast.Module, ast.FunctionDef]
    FORBIDDEN_LEVEL = 3
    DIFF = 2

    @classmethod
    def make_all(cls, module, data, directory):
        classes_names = cls.get_classes(module)
        funcs = cls.find_all_functions_module(module)
        data['classes'] += len(classes_names)
        data['functions'] += len(funcs)
        unpls = [directory + "#" + n for n in cls.find_unpleasant_funcs(funcs)]
        data['unpleasant_functions'].extend(unpls)

    @classmethod
    def find_all_functions_module(cls, module):
        classes_names = cls.get_classes(module)
        functions = cls.get_functions(module)
        functions = list(map(lambda x: getattr(module, x), functions))
        for c in classes_names:
            clss = getattr(module, c)
            funcs = cls.get_functions(clss)
            functions.extend(list(map(lambda x: getattr(clss, x), funcs)))
        return functions

    @classmethod
    def get_classes(cls, module):
        classes = list(map(lambda x: x[0],
                           inspect.getmembers(module,
                                              predicate=inspect.isclass)))
        return classes

    @classmethod
    def get_functions(cls, module):
        functions = list(map(lambda x: x[0],
                             inspect.getmembers(module,
                                                predicate=inspect.isfunction)))
        return functions

    @classmethod
    def find_unpleasant_funcs(cls, functions):
        funcs = []
        for func in functions:
            if not cls.is_pleasant(func):
                funcs.append(func.__name__)
        return funcs

    @classmethod
    def is_pleasant(cls, function_name):
        cls.DIFF = -1
        function_ast = ast.parse(
            textwrap.dedent(inspect.getsource(function_name)))
        queue = [(function_ast, cls.DIFF)]
        return cls.go_through_function_util(queue)

    @classmethod
    def go_through_function_util(cls, queue):
        while queue:
            element, level = queue.pop()
            if level >= cls.FORBIDDEN_LEVEL and type(element) in cls.GATES:
                return False

            if hasattr(element, 'body') and type(element) in cls.GATES:
                for inner in element.body:
                    queue.append((inner, level + 1))
        return True

print(stats('/home/desi/pyhom'))
