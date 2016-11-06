# -*- coding: utf-8 -*-

"""
expressions
----------------------------------

Parser definition for funcparserlib. The parsers that need forward declaration
are defined as function annotated by the `Parser` decorator

The definitions are specified in the Appendix B.2.7 of the Modelica
Specification 3.3.
"""

from funcparserlib.parser import many, maybe, Parser

# pylint: disable=no-name-in-module, missing-docstring
from modparc.syntax import keyword, op, token_type
from modparc.syntax.syntax_elements import (Expression, SimpleExpression,
                                            LogicalExpression, LogicalTerm,
                                            LogicalFactor, Relation,
                                            ArithmeticExpression, Term, Factor,
                                            Primary, RelOp, MulOp, AddOp, Name,
                                            NamedArgument, NamedArguments,
                                            FunctionArgument,
                                            FunctionArguments,
                                            FunctionCallArgs, ExpressionList,
                                            OutputExpressionList, Subscript,
                                            ArraySubscript, ComponentReference,
                                            StringComment, Annotation, Comment)
# pylint: enable=no-name-in-module

name = (maybe(op(".")) + (token_type("ident") | keyword("assert")) +
        maybe(many(op(".") + (token_type("ident") | keyword("assert"))))
        >> Name)

rel_op = op("<") | op("<=") | op(">") | op(">=") | op("==") | op("<>") >> RelOp

add_op = op("+") | op("-") | op(".+") | op(".-") >> AddOp

mul_op = op("*") | op("/") | op(".*") | op("./") >> MulOp


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

    return (parser >> Primary).run(tokens, state)

factor = primary + maybe((op("^") | op(".^")) + primary) >> Factor

term = factor + maybe(many(mul_op + factor)) >> Term

arithmetic_expression = (maybe(add_op) + term + maybe(many(add_op + term))
                         >> ArithmeticExpression)

relation = (arithmetic_expression + maybe(rel_op + arithmetic_expression)
            >> Relation)

logical_factor = maybe(keyword("not")) + relation >> LogicalFactor

logical_term = (logical_factor + maybe(many(keyword("and") + logical_factor))
                >> LogicalTerm)

logical_expression = (logical_term + maybe(many(keyword("or") + logical_term))
                      >> LogicalExpression)

simple_expression = (logical_expression + maybe(op(":") + logical_expression
                                                + maybe(op(":") +
                                                        logical_expression))
                     >> SimpleExpression)


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
    return (parser >> NamedArgument).run(tokens, state)

named_arguments = (named_argument + maybe(many(op(",") + named_argument))
                   >> NamedArguments)


@Parser
def function_argument(tokens, state):
    parser = (keyword("function") + name +
              op('(') + maybe(named_arguments) + op(')')
              | expression)
    return (parser >> FunctionArgument).run(tokens, state)


@Parser
def function_arguments(tokens, state):
    from modparc.syntax.equations import for_indices  # circular dependency
    # Since funcparserlib doesn't have full backtracking
    # the `named_arguments` parser is matched first to avoid problems
    parser = (named_arguments
              | function_argument +
              maybe(op(",") + function_arguments
                    | keyword('for') + for_indices))
    return (parser >> FunctionArguments).run(tokens, state)


function_call_args = (op("(") + maybe(function_arguments) + op(")")
                      >> FunctionCallArgs)

expression_list = (expression + maybe(many(op(",") + expression))
                   >> ExpressionList)

output_expression_list = (maybe(expression) +
                          maybe(many(op(",") + maybe(expression)))
                          >> OutputExpressionList)


subscript = op(":") | expression >> Subscript

array_subscript = (op("[") + subscript +
                   maybe(many(op(',') + subscript)) + op("]")
                   >> ArraySubscript)

component_reference = (maybe(op('.')) + token_type('ident') +
                       maybe(array_subscript) +
                       maybe(many(op('.') + token_type('ident') +
                                  maybe(array_subscript)))
                       >> ComponentReference)

string_comment = (maybe(token_type("string") +
                        maybe(many(op("+") + token_type("string"))))
                  >> StringComment)


@Parser
def annotation(tokens, state):
    from .modification import class_modification  # circular dependency
    parser = keyword('annotation') + class_modification >> Annotation
    return parser.run(tokens, state)


comment = string_comment + maybe(annotation) >> Comment
