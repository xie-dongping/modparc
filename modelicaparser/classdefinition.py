# -*- coding: utf-8 -*-

from funcparserlib.lexer import Token
from funcparserlib.parser import (some, a, many, skip, finished, maybe,
                                  with_forward_decls, Parser)
from syntax import keyword, op, token_type

from expressions import name

class Statement(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.text = " ".join([tok.value for tok in tokens])
    def __str__(self):
            return "{0}({1})".format(self.__class__.__name__, self.text)

class ClassPrefix(Statement):
    pass

@Parser
def class_prefix(tokens, state):
    k = keyword
    km = lambda key: maybe(keyword(key))
    function_prefix = (maybe(k("pure") | k("impure")) + km("operator")
                       + k("function"))
    parser = km("partial") + (k("class") | k("model") |
                              (km("operator") + k("record")) |
                              k("block") |
                              (km("expandable") + k("connector")) |
                              k("type") | k("type") |
                              (km("expandable") + k("connector")) |
                              function_prefix | k("operator"))

    return (parser >> ClassPrefix).run(tokens, state)


@Parser
def enumeration_literal(tokens, state):
    parser = token_type("ident") + token_type("comment")
    return parser.run(tokens, state)


@Parser
def enum_list(tokens, state):
    parser = enumeration_literal + maybe(many(op(",") +
                                         enumeration_literal))
    return parser.run(tokens, state)

@Parser
def language_specification(tokens, state):
    parser = token_type('string')
    return parser.run(tokens, state)

#@Parser
#def element_list(tokens, state):
#    parser = maybe(many(element + op(';')))
#    return parser.run(tokens, state)
#
#@Parser
#def element(tokens, state):
#    k = keyword
#    km = lambda key: maybe(keyword(key))
#    parser = (import_clause | 
#              extends_clause | 
#              km('redeclare') + km('final') + 
#              km('inner') + km('outer') + 
#              ((class_definition | component_clause) |
#               k('replaceable') + (class_definition | 
#                                   component_clause) 
#               + maybe(constraining_clause + comment)))
#    return parser.run(tokens, state)

@Parser
def import_clause(tokens, state):
    parser = (keyword('import') +
              (token_type("ident") + op('=') + name |
               name + maybe(op(".") + (op("*") |
                                       op("{") + import_list + op("}")))
              + token_type('comment')))
    return parser.run(tokens, state)

@Parser
def import_list(tokens, state):
    parser = (token_type("ident") + maybe(many(op(",") +
                                          token_type("ident"))))
    return parser.run(tokens, state)


# def parse(tokens):
#     'Sequence(Token) -> int or float or None'
#     # Well known functions
#     const = lambda x: lambda _: x
#     tokval = lambda tok: tok.value
#     makeop = lambda s, f: op(s) >> const(f)
# 
#     def eval_expr(z, list):
#      'float, [((float, float -> float), float)] -> float'
#      return reduce(lambda s, (f, x): f(s, x), list, z)
# 
#     # Primitives
#     number = (
#      some(lambda tok: tok.code == token.NUMBER)
#      >> tokval
#      >> make_number)
#     op = lambda s: a(Token(token.OP, s)) >> tokval
#     op_ = lambda s: skip(op(s))
# 
#     add = makeop('+', operator.add)
#     sub = makeop('-', operator.sub)
#     mul = makeop('*', operator.mul)
#     div = makeop('/', operator.div)
#     pow = makeop('**', operator.pow)
# 
#     mul_op = mul | div
#     add_op = add | sub
# 
#     # Means of composition
#     @with_forward_decls
#     def primary():
#      return number | (op_('(') + expr + op_(')'))
#     factor = primary + many(pow + primary) >> eval
#     term = factor + many(mul_op + factor) >> eval
#     expr = term + many(add_op + term) >> eval
# 
#     # Toplevel parsers
#     endmark = a(Token(token.ENDMARKER, ''))
#     end = skip(endmark + finished)
#     toplevel = maybe(expr) + end
# 
#     return toplevel.parse(tokens)
# 
