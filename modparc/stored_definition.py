# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from funcparserlib.parser import many, maybe, skip, finished

from .syntax import keyword, op
from .expressions import name
from .class_definition import class_definition

# pylint: disable=no-name-in-module
from .syntax_elements import StoredDefinition
# pylint: enable=no-name-in-module

stored_definition = (maybe(keyword("within") + maybe(name) + op(";")) +
                     maybe(many(maybe(keyword("final")) +
                                class_definition + op(";"))) + skip(finished)
                     >> StoredDefinition)
