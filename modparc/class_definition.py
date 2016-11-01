# -*- coding: utf-8 -*-

from funcparserlib.parser import many, maybe, Parser

from .syntax import keyword, op, token_type

from .expressions import (name, comment, annotation, string_comment, 
                          component_reference, array_subscript, 
                          expression_list)
from .component_clause import type_prefix, component_clause
from .extends import extends_clause, constraining_clause
from .equations import equation_section, algorithm_section
from .modification import class_modification


class Statement(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.text = " ".join([tok.value for tok in tokens])

    def __str__(self):
            return "{0}({1})".format(self.__class__.__name__, self.text)


class ClassPrefix(Statement):
    pass

language_specification = token_type('string')

base_prefix = type_prefix

external_function_call = (maybe(component_reference + op("=")) +
                          token_type('indent') + op("(") +
                          maybe(expression_list) + op(")"))


@Parser
def class_definition(tokens, state):
    parser = maybe(keyword("encapsulated")) + class_prefixes + class_specifier
    return parser.run(tokens, state)


@Parser
def element(tokens, state):
    k = keyword
    km = lambda key: maybe(keyword(key))
    parser = (import_clause |
              extends_clause |
              km('redeclare') + km('final') +
              km('inner') + km('outer') +
              ((class_definition | component_clause) |
               k('replaceable') + (class_definition |
                                   component_clause)
               + maybe(constraining_clause + comment)))
    return parser.run(tokens, state)

element_list = maybe(many(element + op(';')))

composition = (element_list +
               maybe(many(keyword("public") + element_list |
                          keyword("protected") + element_list |
                          equation_section |
                          algorithm_section)) +
               maybe(keyword("external") + maybe(language_specification) +
                     maybe(external_function_call) + maybe(annotation) +
                     op(";")) +
               maybe(annotation + op(";")))


@Parser
def class_specifier(tokens, state):
    normal = (token_type('ident') + string_comment + composition
              + keyword('end') + token_type('ident'))
    derived = (token_type('ident') + op("=") + base_prefix + name +
               maybe(array_subscript) + maybe(class_modification) + comment)
    enum_def = (token_type('ident') + op("=") + keyword('enumeration')
                + op("(") + (maybe(enum_list) | op(":")) + op(")") + comment)
    derivative = (token_type('ident') + op("=") + keyword('der')
                  + op("(") + name + op(",") + token_type('ident')
                  + maybe(many(op(",") + token_type('ident')))
                  + op(")") + comment)
    extended = (keyword('extends') + token_type('ident') +
                maybe(class_modification) + string_comment + composition +
                keyword("end") + token_type('ident'))

    parser = (normal | derived | enum_def | derivative | extended)
    return parser.run(tokens, state)


@Parser
def class_prefixes(tokens, state):
    kw = keyword
    km = lambda key: maybe(keyword(key))
    function_prefix = (maybe(kw("pure") | kw("impure")) + km("operator")
                       + kw("function"))
    parser = (km("partial") + (kw("class") | kw("model") |
              (km("operator") + kw("record")) |
              kw("block") |
              (km("expandable") + kw("connector")) |
              kw("type") | kw("type") |
              (km("expandable") + kw("connector")) |
              function_prefix | kw("operator")))

    return parser.run(tokens, state)


enumeration_literal = token_type("ident") + comment

enum_list = enumeration_literal + maybe(many(op(",") +
                                        enumeration_literal))



import_list = (token_type("ident") + maybe(many(op(",") +
                                           token_type("ident"))))

import_clause = (keyword('import') +
                 (token_type("ident") + op('=') + name |
                  name + maybe(op(".") + (op("*") |
                                          op("{") + import_list + op("}")))
                 + comment))
