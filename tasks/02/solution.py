import operator


class MathOperation:
    SYMBOLS_FUNCS = {
        '__add__': '+', '__radd__': '+', '__sub__': '-', '__rsub__': '-',
        '__mul__': '*', '__rmul__': '*', '__truediv__': '/',
        '__rtruediv__': '/', '__div__': '/', '__rdiv__': '/',
        '__mod__': '%', '__rmod__': '%', '__pow__': '**', '__rpow__': '**',
        '__floordiv__': '//', '__lshift__': '<<', '__rshift__': '>>',
        '__and__': '&', '__xor__': '^', '__or__': '|',
        '__rfloordiv__': '//', '__rlshift__': '<<', '__rrshift__': '>>',
        '__rand__': '&', '__rxor__': '^', '__ror__': '|',
    }
    FUNCTIONS = ['__add__', '__sub__', '__mul__', '__truediv__', '__div__',
                 '__mod__', '__pow__', '__floordiv__', '__lshift__',
                 '__rshift__', '__and__', '__xor__', '__or__']
    RFUNCTIONS = ['__radd__', '__rsub__', '__rmul__', '__rtruediv__',
                  '__rdiv__', '__rmod__', '__rpow__', '__rfloordiv__',
                  '__rlshift__', '__rrshift__', '__rand__',
                  '__rxor__', '__ror__']

    def _add_functions(self):
        for func_name in type(self).FUNCTIONS:
            setattr(type(self), func_name, self.__make_func(func_name,
                                                            func_name))

        for index, func_name in enumerate(type(self).RFUNCTIONS, start=0):
            setattr(type(self), func_name,
                    self.__make_func(type(self).FUNCTIONS[index],
                                     func_name, -1))

    def __make_func(self, func_name, func_named, way=1):
        def func(self, other):
            args = [self, Operator(type(self).SYMBOLS_FUNCS[func_name],
                                   getattr(operator, func_name)),
                    other]
            return Expression(tuple(args[::way]))
        func.__name__ = func_named
        return func


class Constant(MathOperation):
    def __init__(self, value):
        self.VALUE = value
        self._add_functions()

    def evaluate(self, **kwargs):
        return self.VALUE

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.VALUE)


class Expression(MathOperation):

    def __init__(self, expression):
        self.expression = self.__make_expresion(expression)
        self.variable_names = self.__collect_variable_names()
        self._add_functions()

    def __str__(self):
        if isinstance(self.expression, tuple):
            return "({} {} {})".format(str(self.expression[0]),
                                       str(self.expression[1]),
                                       str(self.expression[2]))
        return str(self.expression)

    def __repr__(self):
        return str(self)

    def __make_expresion(self, expression):
        if isinstance(expression, tuple):
            return (Expression(expression[0]),
                    expression[1],
                    Expression(expression[2]))
        return expression

    def __collect_variable_names(self):
        VAR_NAMES = {
            Constant: lambda ex: [],
            Variable: lambda ex: ex.variable_names,
            tuple: lambda ex: ex[0].variable_names + ex[2].variable_names,
            Expression: lambda ex: ex.variable_names
        }
        function = VAR_NAMES.get(type(self.expression), lambda ex: [])
        return function(self.expression)

    def evaluate(self, **kwargs):
        DEFINED_TYPES = (Expression, Variable, Constant, tuple)
        if not type(self.expression) in DEFINED_TYPES:
            return self.expression
        elif not isinstance(self.expression, tuple):
            return self.expression.evaluate(**kwargs)
        return (self.expression[1]((self.expression[0]).evaluate(**kwargs),
                                   (self.expression[2]).evaluate(**kwargs)))


class Variable(MathOperation):

    def __init__(self, name):
        self.NAME = name
        self._add_functions()

    @property
    def variable_names(self):
        return [self.NAME]

    def __str__(self):
        return self.NAME

    def __repr__(self):
        return str(self)

    def evaluate(self, **kwargs):
        return kwargs[self.NAME]


class Operator:
    def __init__(self, symbol, logic):
        self.symbol = symbol
        self.logic = logic

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol

    def __call__(self, lhs, rhs):
        return self.logic(lhs, rhs)


def create_operator(symbol, logic):
    return Operator(symbol, logic)


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_expression(expression_structure):
    return Expression(expression_structure)

x = create_variable('x')
y = create_variable('y')
z = create_variable('z')
k = create_variable('k')
plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
f = (z - (y - k)) + z
# 2 << 3
variables = f.variable_names
twelve = create_constant(12)
times = create_operator('*', lambda lhs, rhs: lhs * rhs)
expression = create_expression((x, plus, (y, times, twelve)))
print(f.evaluate(x=1, z=2, y=3, k=1, b=6))
print(variables)
print(f)
print(expression)
#print(Expression.__dict__)
