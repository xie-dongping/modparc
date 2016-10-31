# -*- coding: utf-8 -*-

from funcparserlib.parser import many, maybe, finished

from .syntax import keyword, op
from .expressions import name
from .class_definition import class_definition

stored_definition = (maybe(keyword("within") + maybe(name) + op(";")) +
                     maybe(many(maybe(keyword("final")) +
                                class_definition + op(";"))) +
                     finished)
