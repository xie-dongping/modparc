# -*- coding: utf-8 -*-
"""
extends
----------------------------------

Parser definition for funcparserlib. The parsers that need forward declaration
are defined as function annotated by the `Parser` decorator.

The definitions are specified in the Appendix B.2.3 of the Modelica
Specification 3.3.
"""

from funcparserlib.parser import maybe, Parser

# pylint: disable=no-name-in-module, missing-docstring
from modparc.syntax import keyword
from modparc.syntax.expressions import annotation, name
from modparc.syntax.syntax_elements import ExtendsClause, ConstrainingClause
# pylint: enable=no-name-in-module


@Parser
def extends_clause(tokens, state):
    from .modification import class_modification
    parser = (keyword('extends') + name + maybe(class_modification)
              + maybe(annotation)) >> ExtendsClause
    return parser.run(tokens, state)


@Parser
def constraining_clause(tokens, state):
    from .modification import class_modification
    parser = keyword('constrainedby') + name + maybe(class_modification)
    return (parser >> ConstrainingClause).run(tokens, state)
