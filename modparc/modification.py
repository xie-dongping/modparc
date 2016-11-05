# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from funcparserlib.parser import many, maybe, Parser

from .syntax import keyword, op, token_type

from .expressions import (name, expression, string_comment,
                          array_subscript, comment)
from .component_clause import declaration, type_specifier, type_prefix
from .extends import constraining_clause

# pylint: disable=no-name-in-module
from .syntax_elements import (Modification, ShortClassDefinition,
                              ComponentDeclaration1, ComponentClause1,
                              ElementReplaceable, ElementRedeclaration,
                              ElementModification,
                              ElementModificationOrReplaceable,
                              Argument, ArgumentList, ClassModification)
# pylint: enable=no-name-in-module


@Parser
def modification(tokens, state):
    parser = (class_modification + maybe(op('=') + expression)
              | op('=') + expression
              | op(':=') + expression) >> Modification
    return parser.run(tokens, state)


@Parser
def short_class_definition(tokens, state):
    # circular import!
    from .class_definition import class_prefixes, enum_list, base_prefix
    parser = (class_prefixes + token_type("ident") + op("=")
              + (base_prefix + name + maybe(array_subscript)
                 + maybe(class_modification) + comment
                 | keyword('enumeration') + op('(') +
                  (maybe(enum_list) | op(":")) + op(')') + comment))
    return (parser >> ShortClassDefinition).run(tokens, state)

component_declaration1 = declaration + comment >> ComponentDeclaration1

component_clause1 = (type_prefix + type_specifier + component_declaration1
                     >> ComponentClause1)

element_replaceable = (keyword("replaceable") + (short_class_definition
                                                 | component_clause1)
                       + maybe(constraining_clause)) >> ElementReplaceable

element_redeclaration = (keyword("redeclare") + maybe(keyword("each"))
                         + maybe(keyword("final")) +
                         ((short_class_definition | component_clause1
                          | element_replaceable))) >> ElementRedeclaration

element_modification = (name + maybe(modification) + string_comment
                        >> ElementModification)

km = lambda key: maybe(keyword(key))
element_modification_or_replaceable = (km('each') + km('final') +
                                       (element_modification |
                                        element_replaceable)
                                       >> ElementModificationOrReplaceable)

argument = (element_modification_or_replaceable | element_redeclaration
            >> Argument)

argument_list = argument + maybe(many(op(',') + argument)) >> ArgumentList


@Parser
def class_modification(tokens, state):
    parser = op('(') + maybe(argument_list) + op(')') >> ClassModification
    return parser.run(tokens, state)
