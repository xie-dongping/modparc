# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from funcparserlib.parser import maybe, Parser

from .syntax import keyword
from .expressions import annotation, name

# pylint: disable=no-name-in-module
from .syntax_elements import ExtendsClause, ConstrainingClause
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
