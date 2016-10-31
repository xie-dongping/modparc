# -*- coding: utf-8 -*-

from funcparserlib.lexer import Token
from funcparserlib.parser import (some, a, many, skip, finished, maybe,
                                  with_forward_decls, Parser)
from syntax import keyword, op, token_type

name = (op(".", maybe) + token_type("ident") +
        maybe(many(op(".") + token_type("ident"))))

rel_op = op("<") | op("<=") | op(">") | op(">=") | op("==") | op("<>")

add_op = op("+") | op("-") | op(".+") | op(".-") 

mul_op = op("*") | op("/") | op(".*") | op("./") 


