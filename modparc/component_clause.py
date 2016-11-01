# -*- coding: utf-8 -*-

from funcparserlib.parser import (many, maybe, Parser)
from .syntax import keyword, op, token_type

from .expressions import name, comment, expression, array_subscript

kw = keyword

type_prefix = (maybe(kw("flow") | kw("stream")) +
               maybe(kw("discrete") | kw("parameter") | kw("constant")) +
               maybe(kw("input") | kw("output")))

type_specifier = name

condition_attribute = keyword('if') + expression


@Parser
def declaration(tokens, state):
    from .modification import modification
    parser = (token_type('ident') + maybe(array_subscript)
              + maybe(modification))
    return parser.run(tokens, state)

component_declaration = declaration + maybe(condition_attribute) + comment

component_list = component_declaration + maybe(many(op(",") +
                                                    component_declaration))

component_clause = (type_prefix + type_specifier + maybe(array_subscript)
                    + component_list)
