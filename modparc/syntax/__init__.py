# -*- coding: utf-8 -*-
"""
syntax
----------------------------------

The main utilities module for the parser implementation, with tokenizer
and parser creation functions.
"""

from re import MULTILINE

from funcparserlib.lexer import Token
from funcparserlib.parser import some, a, maybe
import funcparserlib.lexer

from modparc.specification import KEYWORDS


def token_type(tok_type):
    """
    Get a parser matching a certain type of tokens

    :param tok_type: predefined token type to be matched
    :return: a parser that matches token of type `tok_type`
    """
    return some(lambda tok: tok.type == tok_type)


def language_element(key, tok_type, combinator=a):
    """
    Parser to match language element by using a certain combinator

    :param key: exact key of the token, e.g.: `begin`, `model`, `)`
    :param tok_type: predefined token type to be matched
    :param combinator: use the combinator to create a parser
    :return: a parser that matches elements using the above condition
    """
    if combinator == a:
        return combinator(Token(tok_type, key))
    elif combinator == some:
        return combinator(lambda tok: tok == Token(tok_type, key))
    elif combinator == maybe:
        return combinator(a(Token(tok_type, key)))
    else:
        raise Exception("Parser creation error")


def keyword(key, combinator=a):
    """
    Parser to match a keyword token with a key and a combinator

    :param key: exact key of the keyword, e.g.: `begin`, `assert` etc.
    :param combinator: use the combinator to create a parser
    :return: a parser that matches a keyword
    """
    return language_element(key, tok_type='keyword', combinator=combinator)


def op(key, combinator=a):
    """
    Parser to match a operator token with a key and a combinator

    :param key: exact key of the operator, e.g.: `+`, `.*` etc.
    :param combinator: use the combinator to create a parser
    :return: a parser that matches an operator
    """
    return language_element(key, tok_type='op', combinator=combinator)


def tokenize(source_code):
    """
    Tokenizer according to Modelica Specification §2 and Appendix B.1

    :param source_code: source code to be tokenized
    :return: list of tokens created
    """
    token_specs = [
        ('string', (r'"([^\\\"]|\\.|[\r\n])*?"', MULTILINE)),
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
        ('op', (r'\.\^',)),
        ('op', (r'[\[\]\.(){}\^+\-*/=\,;\:]',)),
    ]
    inner_tokenize = funcparserlib.lexer.make_tokenizer(token_specs)
    useless = ['comment', 'newline', 'whitespace']

    return [tok for tok in inner_tokenize(source_code)
            if tok.type not in useless]
