# -*- coding: utf-8 -*-
"""
stored_definition
----------------------------------

Parser definition for funcparserlib.

The definitions are specified in the Appendix B.2.1 of the Modelica
Specification 3.3.

This is the top-level module used by in the library api as it parses
the contents of a Modelica source code file (files with suffix .mo).
"""

from funcparserlib.parser import many, maybe, skip, finished

# pylint: disable=no-name-in-module, missing-docstring
from modparc.syntax import keyword, op
from modparc.syntax.class_definition import class_definition
from modparc.syntax.expressions import name
from modparc.syntax.syntax_elements import StoredDefinition
# pylint: enable=no-name-in-module

stored_definition = (maybe(keyword("within") + maybe(name) + op(";")) +
                     many(maybe(keyword("final")) +
                          class_definition + op(";")) + skip(finished)
                     >> StoredDefinition)
