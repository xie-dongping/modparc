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
        ('ident', (r"'" + r'([a-zA-Z_0-9' +
                   r'!#%&()*+,\-\./:;<>=?@\[\]\^{}|~ ' +
                   r'\"\?\\\a\b\f\n\r\t\v]|[^\\"]|\\.)*' + r"'",)),
        ('comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('comment', (r'//.*',)),
        ('newline', (r'[\r\n]+',)),
        ('whitespace', (r'[ \t\r\n]+',)),
        ('keyword', (r'(' + r'\b|'.join(KEYWORDS) + r'\b)',)),
        ('ident', (r'[a-zA-Z_][a-zA-Z_0-9]*',)),
        ('number', (r'\d+(\.\d+)?([eE]\d+)?',)),
        ('op', (r'(<>|<=|>=|==)',)),
        ('op', (r'[<>]',)),
        ('op', (r'(\.\+|\.-)',)),
        ('op', (r'[+\-]',)),
        ('op', (r'(\.\*|\./)',)),
        ('op', (r'[:=]',)),
        ('op', (r'[*/]',)),
        ('op', (r'[\[\]\.(){}\^+\-*/=\,;:]',)),
    ]
    inner_tokenize = funcparserlib.lexer.make_tokenizer(token_specs)
    useless = ['comment', 'newline', 'whitespace']

    return [tok for tok in inner_tokenize(string) if tok.type not in useless]


def get_all_models(root_path):
    import os
    file_list = [os.path.join(path, fn)
                 for path, _, filenames in os.walk(root_path)
                 for fn in filenames
                 if fn.endswith('.mo')]
    return file_list


def print_file(file_name, function=tokenize):
    with open(file_name, 'r') as f:
        content = f.read()
        results = function(content)
        pprint.pprint(results)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run it on modelica files')
    parser.add_argument('root_path', type=str, nargs='?',
                        help='Root path for Modelica libraries')

    args = parser.parse_args().__dict__

    if args.get('root_path') is None:
        MODELICA_PATH = "***REMOVED***/workspace/modelica/"
        path = MODELICA_PATH
    else:
        path = args['root_path']

    file_list = get_all_models(path)

    for f_name in file_list:
        print("File name is {0}".format(f_name))
        print_file(f_name, function=tokenize)
