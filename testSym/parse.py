import re
from sympy import Symbol
from sympy.logic.boolalg import *

token_pat = re.compile("\s*(?:([a-z])|([|&~]|=>))")


def tokenize(program):
    for variable, operator in token_pat.findall(program):
        if variable:
            yield literal_token(variable)
        elif operator == "|":
            yield operator_or_token()
        elif operator == "&":
            yield operator_and_token()
        elif operator == "=>":
            yield operator_implies_token()
        elif operator == "~":
            yield operator_not_token()
        elif operator == '(':
            yield operator_lparen_token()
        elif operator == ')':
            yield operator_rparen_token()
        else:
            raise SyntaxError('unknown operator: ' + operator)
    yield end_token()


def match(tok=None):
    global gen, token
    if tok and tok != type(token):
        raise SyntaxError('Expected %s' % tok)
    token = gen.__next__()


def parse(program):
    global gen, token
    gen = tokenize(program)
    token = gen.__next__()

    return expression()


def expression(rbp=0):
    global token
    t = token
    token = gen.__next__()
    left = t.nud()
    try:
        while rbp < token.lbp:
            t = token
            token = gen.__next__()
            left = t.led(left)
    except Exception:
        raise
    return left


class literal_token(object):
    def __init__(self, value):
        self.value = value

    def nud(self):
        return 'var', self.value


class operator_or_token(object):
    lbp = 2

    def led(self, left):
        right = expression(2)
        return 'or', left, right


class operator_not_token(object):
    lbp = 3

    def nud(self):
        right = expression(3)
        return 'not', right


class operator_and_token(object):
    lbp = 2

    def led(self, left):
        right = expression(2)
        return 'and', left, right


class operator_implies_token(object):
    lbp = 1

    def led(self, left):
        right = expression(1)
        return 'implies', left, right


class operator_lparen_token(object):
    lbp = 0

    def nud(self):
        expr = expression()

        match(operator_rparen_token)
        return expr


class operator_rparen_token(object):
    lbp = 0


class end_token(object):
    lbp = 0


ASTOPS = {
    'not': Not,
    'or': Or,
    'and': And,
    'implies': Implies,
}
_CONSTS = [BooleanFalse, BooleanTrue]


def parse_expr(s):
    ast = parse(s)
    return ast2expr(ast)


def ast2expr(ast):
    """Convert an abstract syntax tree to an Expression."""
    if ast[0] == 'const':
        return _CONSTS[ast[1]]
    elif ast[0] == 'var':
        return Symbol(ast[1])
    else:
        xs = [ast2expr(x) for x in ast[1:]]
        return ASTOPS[ast[0]](*xs)


if __name__ == '__main__':
    # program = '~p & q => a'
    # for variable, operator in token_pat.findall(program):
    #     print(variable, operator)
    try:
        print(parse_expr('p & q => a | v | ~s & r | t'))
    except SyntaxError as e:
        print('fail' + e.msg)
