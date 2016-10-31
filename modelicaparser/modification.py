# -*- coding: utf-8 -*-

from funcparserlib.parser import many, maybe, Parser
from syntax import keyword, op, token_type

from expressions import (name, expression, string_comment,
                         array_subscript, comment)
from class_definition import class_prefix, enum_list, base_prefix
from component_clause import declaration, type_specifier, type_prefix
from extends import constraining_clause


@Parser
def modification(tokens, state):
    parser = (class_modification + maybe(op('=') + expression)
              | op('=') + expression
              | op(':=') + expression)
    return parser.run(tokens, state)


@Parser
def short_class_definition(tokens, state):
    parser = (class_prefix + token_type("ident") + op("=")
              + (base_prefix + name + maybe(array_subscript)
                 + maybe(class_modification) + comment
                 | keyword('enumeration') + op('(') +
                  (maybe(enum_list) | op(":")) + op(')') + comment))
    return parser.run(tokens, state)

component_declaration1 = declaration + comment

component_clause1 = type_prefix + type_specifier + component_declaration1

element_replaceable = (keyword("replaceable") + (short_class_definition
                                                 | component_clause1)
                       + maybe(constraining_clause))

element_redeclaration = (keyword("replaceable") + maybe(keyword("each"))
                         + maybe(keyword("final")) +
                         ((short_class_definition | component_clause1
                          | element_replaceable)))


element_modification = name + maybe(modification) + string_comment

km = lambda key: maybe(keyword(key))
element_modification_or_replaceable = (km('each') + km('final') +
                                       (element_modification |
                                        element_replaceable))

argument = element_modification_or_replaceable | element_redeclaration

argument_list = argument + maybe(many(op(',') + argument))


@Parser
def class_modification(tokens, state):
    parser = op('(') + maybe(argument_list) + op(')')
    return parser.run(tokens, state)
