# -*- coding: utf-8 -*-

from funcparserlib.parser import many, maybe, Parser
from .syntax import keyword, op, token_type

from .expressions import (expression, simple_expression, name, comment,
                         function_call_args, component_reference,
                         output_expression_list)

for_index = token_type('indent') + maybe(keyword('in') + expression)

for_indices = for_index + maybe(many(op(',') + for_index))

connect_clause = (keyword("connect") + op("(") + component_reference
                  + op(",") + component_reference + op(")"))


@Parser
def equation(tokens, state):
    parser = ((simple_expression + op("=") + expression
               | if_equation
               | for_equation
               | connect_clause
               | when_equation
               | name + function_call_args)
              + comment)
    return parser.run(tokens, state)


@Parser
def if_equation(tokens, state):
    kw = keyword
    parser = (kw("if") + expression + kw("then") +
              maybe(many(equation + op(";"))) +
              maybe(many(kw("elseif") + expression + kw("then") +
                         maybe(many(equation + op(";"))))) +
              maybe(kw("else") +
                    maybe(many(equation + op(";")))) +
              kw("end") + kw("if"))
    return parser.run(tokens, state)


@Parser
def for_equation(tokens, state):
    kw = keyword
    parser = (kw("for") + for_indices + kw("loop") +
              maybe(many(equation + op(";"))) +
              kw("end") + kw("for"))
    return parser.run(tokens, state)


@Parser
def while_equation(tokens, state):
    kw = keyword
    parser = (kw("while") + expression + kw("loop") +
              maybe(many(equation + op(";"))) +
              kw("end") + kw("while"))
    return parser.run(tokens, state)


@Parser
def when_equation(tokens, state):
    kw = keyword
    parser = (kw("when") + expression + kw("then") +
              maybe(many(equation + op(";"))) +
              maybe(many(kw("elsewhen") + expression + kw("then") +
                         maybe(many(equation + op(";"))))) +
              kw("end") + kw("when"))
    return parser.run(tokens, state)


@Parser
def statement(tokens, state):
    parser = ((component_reference + (op(":=") + expression
                                      | function_call_args)
               | (op('(') + output_expression_list + op('(') + op(':=')
                  + component_reference + function_call_args)
               | keyword('break')
               | keyword('return')
               | if_statement
               | for_statement
               | connect_clause
               | when_statement)
              + comment)
    return parser.run(tokens, state)


@Parser
def if_statement(tokens, state):
    kw = keyword
    parser = (kw("if") + expression + kw("then") +
              maybe(many(statement + op(";"))) +
              maybe(many(kw("elseif") + expression + kw("then") +
                         maybe(many(statement + op(";"))))) +
              maybe(kw("else") +
                    maybe(many(statement + op(";")))) +
              kw("end") + kw("if"))
    return parser.run(tokens, state)


@Parser
def for_statement(tokens, state):
    kw = keyword
    parser = (kw("for") + for_indices + kw("loop") +
              maybe(many(statement + op(";"))) +
              kw("end") + kw("for"))
    return parser.run(tokens, state)


@Parser
def while_statement(tokens, state):
    kw = keyword
    parser = (kw("while") + expression + kw("loop") +
              maybe(many(statement + op(";"))) +
              kw("end") + kw("while"))
    return parser.run(tokens, state)


@Parser
def when_statement(tokens, state):
    kw = keyword
    parser = (kw("when") + expression + kw("then") +
              maybe(many(statement + op(";"))) +
              maybe(many(kw("elsewhen") + expression + kw("then") +
                         maybe(many(statement + op(";"))))) +
              kw("end") + kw("when"))
    return parser.run(tokens, state)

equation_section = (maybe(keyword("initial")) + keyword("equation") +
                    maybe(many(equation + op(';'))))

algorithm_section = (maybe(keyword("initial")) + keyword("algorithm") +
                     maybe(many(statement + op(';'))))
