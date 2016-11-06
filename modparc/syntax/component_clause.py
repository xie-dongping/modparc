# -*- coding: utf-8 -*-
"""
component_clause
----------------------------------

Parser definition for funcparserlib. The parsers that need forward declaration
are defined as function annotated by the `Parser` decorator.

The definitions are specified in the Appendix B.2.4 of the Modelica
Specification 3.3.
"""

from funcparserlib.parser import (many, maybe, Parser)

# pylint: disable=no-name-in-module, missing-docstring
from modparc.syntax import keyword, op, token_type
from modparc.syntax.expressions import (name, comment, expression,
                                        array_subscript)
from modparc.syntax.syntax_elements import (TypePrefix, TypeSpecifier,
                                            ConditionAttribute, Declaration,
                                            ComponentDeclaration,
                                            ComponentList, ComponentClause)

# pylint: enable=no-name-in-module

kw = keyword

type_prefix = (maybe(kw("flow") | kw("stream")) +
               maybe(kw("discrete") | kw("parameter") | kw("constant")) +
               maybe(kw("input") | kw("output"))) >> TypePrefix

type_specifier = name >> TypeSpecifier

condition_attribute = keyword('if') + expression >> ConditionAttribute


@Parser
def declaration(tokens, state):
    from .modification import modification
    parser = (token_type('ident') + maybe(array_subscript)
              + maybe(modification)) >> Declaration
    return parser.run(tokens, state)

component_declaration = (declaration + maybe(condition_attribute) + comment
                         >> ComponentDeclaration)

component_list = (component_declaration + maybe(many(op(",") +
                                                     component_declaration))
                  >> ComponentList)

component_clause = (type_prefix + type_specifier + maybe(array_subscript)
                    + component_list) >> ComponentClause
