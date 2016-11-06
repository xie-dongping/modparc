#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-name-in-module, missing-docstring
"""
class_definition
----------------------------------

Parser definition for funcparserlib. The parsers that need forward declaration
are defined as function annotated by the `Parser` decorator.

The definitions are specified in the Appendix B.2.2 of the Modelica
Specification 3.3.
"""


from funcparserlib.parser import many, maybe, Parser

from modparc.syntax import keyword, op, token_type
from modparc.syntax.component_clause import type_prefix, component_clause
from modparc.syntax.equations import equation_section, algorithm_section
from modparc.syntax.expressions import (name, comment, annotation,
                                        string_comment, component_reference,
                                        array_subscript, expression_list)
from modparc.syntax.extends import extends_clause, constraining_clause
from modparc.syntax.modification import class_modification
from modparc.syntax.syntax_elements import (LanguageSpecification, BasePrefix,
                                            ExternalFunctionCall,
                                            ClassDefinition, Element,
                                            ElementList, Composition,
                                            ClassSpecifier, ClassPrefixes,
                                            EnumerationLiteral, EnumList,
                                            ImportList, ImportClause)
# pylint: enable=no-name-in-module

language_specification = token_type('string') >> LanguageSpecification

base_prefix = type_prefix >> BasePrefix

external_function_call = (maybe(component_reference + op("=")) +
                          token_type('ident') + op("(") +
                          maybe(expression_list) + op(")")
                          >> ExternalFunctionCall)


@Parser
def class_definition(tokens, state):
    parser = maybe(keyword("encapsulated")) + class_prefixes + class_specifier
    return (parser >> ClassDefinition).run(tokens, state)


def km(key):
    return maybe(keyword(key))


@Parser
def element(tokens, state):
    kw = keyword
    parser = (import_clause |
              extends_clause |
              km('redeclare') + km('final') +
              km('inner') + km('outer') +
              ((class_definition | component_clause) |
               kw('replaceable') + (class_definition |
                                    component_clause)
               + maybe(constraining_clause + comment)))
    return (parser >> Element).run(tokens, state)

element_list = maybe(many(element + op(';'))) >> ElementList

composition = (element_list +
               maybe(many(keyword("public") + element_list |
                          keyword("protected") + element_list |
                          equation_section |
                          algorithm_section)) +
               maybe(keyword("external") + maybe(language_specification) +
                     maybe(external_function_call) + maybe(annotation) +
                     op(";")) +
               maybe(annotation + op(";")) >> Composition)


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
    return (parser >> ClassSpecifier).run(tokens, state)


@Parser
def class_prefixes(tokens, state):
    kw = keyword
    function_prefix = (maybe(kw("pure") | kw("impure")) + km("operator")
                       + kw("function"))
    parser = (km("partial")
              + ((kw("class") | kw("model") |
                  km("operator") + kw("record") |
                  kw("block") |
                  (km("expandable") + kw("connector")) |
                  kw("type") | kw("package") |
                  function_prefix | kw("operator"))))

    return (parser >> ClassPrefixes).run(tokens, state)

enumeration_literal = token_type("ident") + comment >> EnumerationLiteral

enum_list = enumeration_literal + maybe(many(op(",") +
                                             enumeration_literal)) >> EnumList

import_list = (token_type("ident") + maybe(many(op(",") +
                                                token_type("ident")))
               >> ImportList)

import_clause = (keyword('import') +
                 (token_type("ident") + op('=') + name |
                  name + maybe(op(".*")
                               | op(".") + op("{") + import_list + op("}")))
                 + comment) >> ImportClause
