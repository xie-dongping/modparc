# -*- coding: utf-8 -*-

from funcparserlib.lexer import Token
from funcparserlib.parser import some, a, maybe
import funcparserlib.lexer
from re import MULTILINE
import pprint

from .specification import KEYWORDS


def token_type(tok_type):
    "Match the token of a certain type"
    return some(lambda tok: tok.type == tok_type)


def language_element(key, tok_type, combinator=a):
    "Type to match language element by using a certain combinator"
    if combinator == a:
        return combinator(Token(tok_type, key))
    elif combinator == some:
        return combinator(lambda tok: tok == Token(tok_type, key))
    elif combinator == maybe:
        return combinator(a(Token(tok_type, key)))
    else:
        raise Exception("Parse error")


def keyword(key, combinator=a):
    "Match the keyword tokens"
    return language_element(key, tok_type='keyword', combinator=combinator)


def op(key, combinator=a):
    "Match the operator tokens"
    return language_element(key, tok_type='op', combinator=combinator)


def tokenize(string):
    token_specs = [
        ('string', (r'"([^\\"]|\\.|[\r\n])*?"', MULTILINE)),
        ('comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('ident', (r"'" + r'([a-zA-Z_0-9' +
                   r'!#%&()*+,\-\./:;<>=?@\[\]\^{}|~ ' +
                   r'\"\?\\\a\b\f\n\r\t\v])*' + r"'",)),  # TODO: Unicode
        ('comment', (r'//.*',)),
        ('newline', (r'[\r\n]+',)),
        ('whitespace', (r'[ \t\r\n]+',)),
        ('keyword', (r'(' + r'\b|'.join(KEYWORDS) + r'\b)',)),
        ('number', (r'\d+(\.(\d+)?)?([eE][\+-]?\d+)?',)),
        ('ident', (r'[a-zA-Z_][a-zA-Z_0-9]*',)),
        ('op', (r'(<>|<=|>=|==)',)),
        ('op', (r'[<>]',)),
        ('op', (r'(\.\+|\.-)',)),
        ('op', (r'[+\-]',)),
        ('op', (r'(\.\*|\./)',)),
        ('op', (r':=',)),
        ('op', (r'[*/]',)),
        ('op', (r'[\[\]\.(){}\^+\-*/=\,;\:]',)),
    ]
    inner_tokenize = funcparserlib.lexer.make_tokenizer(token_specs)
    useless = ['comment', 'newline', 'whitespace']

    return [tok for tok in inner_tokenize(string) if tok.type not in useless]
