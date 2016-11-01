# -*- coding: utf-8 -*-

from funcparserlib.parser import many, maybe, Parser
import pprint

from .syntax import keyword, op, token_type


class Expression(object):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        _repr = "{0}: \n{1}".format(super(Expression, self).__repr__(),
                                    pprint.pformat(self.value,
                                                   indent=2))
        return _repr


name = (op(".", maybe) + token_type("ident") +
        maybe(many(op(".") + token_type("ident"))))

rel_op = op("<") | op("<=") | op(">") | op(">=") | op("==") | op("<>")

add_op = op("+") | op("-") | op(".+") | op(".-")

mul_op = op("*") | op("/") | op(".*") | op("./")


@Parser
def primary(tokens, state):
    kw = keyword
    parser = (token_type("number")
              | token_type("string")
              | kw("false")
              | kw("true")
              | (name | kw("der") | kw("initial")) + function_call_args
              | component_reference
              | op("(") + output_expression_list + op(")")
              | (op("[") + expression_list
                 + maybe(many(op(";") + expression_list)) + op("]"))
              | op("{") + function_arguments + op("}")
              | kw("end"))

    return parser.run(tokens, state)


factor = primary + maybe((op("^") | op(".^")) + primary)

term = factor + maybe(many(mul_op + factor))

arithmetic_expression = maybe(add_op) + term + maybe(many(add_op + term))

relation = arithmetic_expression + maybe(rel_op + arithmetic_expression)

logical_factor = maybe(keyword("not")) + relation

logical_term = logical_factor + maybe(many(keyword("and") + logical_factor))

logical_expression = logical_term + maybe(many(keyword("or") + logical_term))

simple_expression = logical_expression + maybe(op(":") + logical_expression
                                               + maybe(op(":") +
                                                       logical_expression))


@Parser
def expression(tokens, state):
    kw = keyword
    parser = (simple_expression
              | kw("if") + expression + kw("then") + expression
              + maybe(many(kw("elseif") + expression
                           + kw("then") + expression))
              + kw("else") + expression) >> Expression
    return parser.run(tokens, state)


@Parser
def named_argument(tokens, state):
    parser = token_type('ident') + op('=') + function_argument
    return parser.run(tokens, state)

named_arguments = named_argument + maybe(many(op(",") + named_argument))


@Parser
def function_argument(tokens, state):
    parser = (keyword("function") + name +
              op('(') + maybe(named_arguments) + op(')')
              | expression)
    return parser.run(tokens, state)


@Parser
def function_arguments(tokens, state):
    from .equations import for_indices  # circular dependency
    parser = (function_argument +
              maybe(op(",") + function_arguments
                    | keyword('for') + for_indices)
              | named_arguments)
    return parser.run(tokens, state)


function_call_args = op("(") + maybe(function_arguments) + op(")")

expression_list = expression + maybe(many(op(",") + expression))

output_expression_list = (maybe(expression) +
                          maybe(many(op(",") + maybe(expression))))

subscript = op(":") | expression

array_subscript = (op("[") + subscript +
                   maybe(many(op(',') + subscript)) + op("]"))

component_reference = (maybe(op('.')) + token_type('ident') +
                       maybe(array_subscript) +
                       maybe(many(op('.') + token_type('ident') +
                                  maybe(array_subscript))))

string_comment = maybe(token_type("string") +
                       maybe(many(op("+") + token_type("string"))))


@Parser
def annotation(tokens, state):
    from .modification import class_modification  # circular dependency
    parser = keyword('annotation') + class_modification
    return parser.run(tokens, state)


comment = string_comment + maybe(annotation)
