# -*- coding: utf-8 -*-

from funcparserlib.parser import maybe, Parser

from syntax import keyword
from expression import annotation, name


@Parser
def extends_clause(tokens, state):
    from modification import class_modification
    parser = (keyword('extends') + name + maybe(class_modification)
              + maybe(annotation))
    return parser.run(tokens, state)


@Parser
def constraining_clause(tokens, state):
    from modification import class_modification
    parser = keyword('constrainedby') + name + maybe(class_modification)
    return parser.run(tokens, state)
