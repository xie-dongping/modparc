# -*- coding: utf-8 -*-
"""
modification
----------------------------------

Parser definition for funcparserlib. The parsers that need forward declaration
are defined as function annotated by the `Parser` decorator

The definitions are specified in the Appendix B.2.5 of the Modelica
Specification 3.3.
"""

from funcparserlib.parser import many, maybe, Parser

# pylint: disable=no-name-in-module, missing-docstring
from modparc.syntax import keyword, op, token_type
from modparc.syntax.component_clause import (declaration, type_specifier,
                                             type_prefix)
from modparc.syntax.expressions import (name, expression, string_comment,
                                        array_subscript, comment)
from modparc.syntax.extends import constraining_clause
from modparc.syntax.syntax_elements import (Modification, ShortClassDefinition,
                                            ComponentDeclaration1,
                                            ComponentClause1,
                                            ElementReplaceable,
                                            ElementRedeclaration,
                                            ElementModification,
                                            ElementModificationOrReplaceable,
                                            Argument, ArgumentList,
                                            ClassModification)
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
    from modparc.syntax.class_definition import (class_prefixes, enum_list,
                                                 base_prefix)
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


def km(key):
    return maybe(keyword(key))

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
