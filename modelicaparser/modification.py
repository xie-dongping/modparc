# -*- coding: utf-8 -*-

from funcparserlib.lexer import Token
from funcparserlib.parser import (some, a, many, skip, finished, maybe,
                                  with_forward_decls, Parser)
from syntax import keyword, op, token_type


