# -*- coding: utf-8 -*-
"""
modparc
----------------------------------

A Modelica parser using parser combinator.
"""
import resource
import sys

import modparc.specification
import modparc.syntax
import modparc.syntax.class_definition
import modparc.syntax.component_clause
import modparc.syntax.equations
import modparc.syntax.expressions
import modparc.syntax.extends
import modparc.syntax.modification
import modparc.syntax.stored_definition  # noqa: F401
from modparc.parse import (parse, parse_file)  # noqa: F401

resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)

__author__ = """谢东平 Dongping XIE"""
__email__ = 'dongping.xie.tud@gmail.com'
__version__ = '0.1.6'
