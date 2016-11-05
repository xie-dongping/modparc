# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from funcparserlib.parser import many, maybe, Parser
from .syntax import keyword, op, token_type

from .expressions import (expression, simple_expression, name, comment,
                          function_call_args, component_reference,
                          output_expression_list)

# pylint: disable=no-name-in-module
from .syntax_elements import (ForIndex, ForIndices, ConnectClause,
                              Equation, IfEquation, ForEquation, WhileEquation,
                              WhenEquation, Statement, IfStatement,
                              ForStatement, WhileStatement, WhenStatement,
                              EquationSection, AlgorithmSection, Assertion)
# pylint: enable=no-name-in-module

for_index = (token_type('ident') + maybe(keyword('in') + expression)
             >> ForIndex)

for_indices = for_index + maybe(many(op(',') + for_index)) >> ForIndices

connect_clause = (keyword("connect") + op("(") + component_reference
                  + op(",") + component_reference + op(")")) >> ConnectClause

assertion = keyword("assert") + function_call_args >> Assertion

@Parser
def equation(tokens, state):
    parser = ((simple_expression + op("=") + expression
               | if_equation
               | for_equation
               | connect_clause
               | when_equation
               | assertion
               | name + function_call_args)
              + comment) >> Equation
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
              kw("end") + kw("if")) >> IfEquation
    return parser.run(tokens, state)


@Parser
def for_equation(tokens, state):
    kw = keyword
    parser = (kw("for") + for_indices + kw("loop") +
              maybe(many(equation + op(";"))) +
              kw("end") + kw("for")) >> ForEquation
    return parser.run(tokens, state)


@Parser
def while_equation(tokens, state):
    kw = keyword
    parser = (kw("while") + expression + kw("loop") +
              maybe(many(equation + op(";"))) +
              kw("end") + kw("while")) >> WhileEquation
    return parser.run(tokens, state)


@Parser
def when_equation(tokens, state):
    kw = keyword
    parser = (kw("when") + expression + kw("then") +
              maybe(many(equation + op(";"))) +
              maybe(many(kw("elsewhen") + expression + kw("then") +
                         maybe(many(equation + op(";"))))) +
              kw("end") + kw("when")) >> WhenEquation
    return parser.run(tokens, state)


@Parser
def statement(tokens, state):
    parser = ((component_reference + (op(":=") + expression
                                      | function_call_args)
               | (op('(') + output_expression_list + op(')') + op(':=')
                  + component_reference + function_call_args)
               | keyword('break')
               | keyword('return')
               | assertion
               | if_statement
               | for_statement
               | while_statement
               | connect_clause
               | when_statement)
              + comment) >> Statement
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
              kw("end") + kw("if")) >> IfStatement
    return parser.run(tokens, state)


@Parser
def for_statement(tokens, state):
    kw = keyword
    parser = (kw("for") + for_indices + kw("loop") +
              maybe(many(statement + op(";"))) +
              kw("end") + kw("for")) >> ForStatement
    return parser.run(tokens, state)


@Parser
def while_statement(tokens, state):
    kw = keyword
    parser = (kw("while") + expression + kw("loop") +
              maybe(many(statement + op(";"))) +
              kw("end") + kw("while")) >> WhileStatement
    return parser.run(tokens, state)


@Parser
def when_statement(tokens, state):
    kw = keyword
    parser = (kw("when") + expression + kw("then") +
              maybe(many(statement + op(";"))) +
              maybe(many(kw("elsewhen") + expression + kw("then") +
                         maybe(many(statement + op(";"))))) +
              kw("end") + kw("when")) >> WhenStatement
    return parser.run(tokens, state)

equation_section = (maybe(keyword("initial")) + keyword("equation") +
                    maybe(many(equation + op(';')))) >> EquationSection

algorithm_section = (maybe(keyword("initial")) + keyword("algorithm") +
                     maybe(many(statement + op(';')))) >> AlgorithmSection
